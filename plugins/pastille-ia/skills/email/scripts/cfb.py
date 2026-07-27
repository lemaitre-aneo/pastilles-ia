"""Écriture d'un conteneur Compound File Binary (CFB / OLE2), version 3.

Le strict nécessaire pour fabriquer un .msg valide: stockages, flux, flux
miniature pour les flux sous le seuil de 4096 octets, chaînes FAT, MiniFAT et
répertoire. Secteurs de 512 octets.
"""
import struct

SECTOR = 512
MINISECTOR = 64
CUTOFF = 4096
FREESECT = 0xFFFFFFFF
ENDOFCHAIN = 0xFFFFFFFE
FATSECT = 0xFFFFFFFD
NOSTREAM = 0xFFFFFFFF

ROOT, STORAGE, STREAM = 5, 1, 2


class Entry:
    def __init__(self, name, kind, data=b"", clsid=b"\x00" * 16):
        assert len(name) <= 31, name
        self.name = name
        self.kind = kind
        self.data = data
        self.clsid = clsid
        self.children = []
        self.idx = NOSTREAM
        self.left = NOSTREAM
        self.right = NOSTREAM
        self.child = NOSTREAM
        self.start = ENDOFCHAIN
        self.size = 0

    def add(self, entry):
        self.children.append(entry)
        return entry


def _key(entry):
    # Ordre CFB: longueur du nom d'abord, puis comparaison insensible à la casse.
    return (len(entry.name), entry.name.upper())


def _ceil(a, b):
    return (a + b - 1) // b


def _build_bst(nodes):
    """Arbre binaire équilibré sur les enfants triés; renvoie l'index racine."""
    if not nodes:
        return NOSTREAM
    mid = len(nodes) // 2
    node = nodes[mid]
    node.left = _build_bst(nodes[:mid])
    node.right = _build_bst(nodes[mid + 1:])
    return node.idx


def _dir_entry(e):
    name = e.name.encode("utf-16-le")
    buf = bytearray(128)
    buf[0:len(name)] = name
    struct.pack_into("<H", buf, 64, len(name) + 2)
    buf[66] = e.kind
    buf[67] = 1  # noir
    struct.pack_into("<III", buf, 68, e.left, e.right, e.child)
    buf[80:96] = e.clsid
    struct.pack_into("<I", buf, 116, e.start)
    struct.pack_into("<Q", buf, 120, e.size)
    return bytes(buf)


def write(root, path):
    entries = []

    def collect(e):
        e.idx = len(entries)
        entries.append(e)
        for c in sorted(e.children, key=_key):
            collect(c)

    collect(root)
    for e in entries:
        kids = sorted(e.children, key=_key)
        e.child = _build_bst(kids) if kids else NOSTREAM

    streams = [e for e in entries if e.kind == STREAM]
    big = [e for e in streams if len(e.data) >= CUTOFF]
    small = [e for e in streams if 0 < len(e.data) < CUTOFF]

    # Flux miniature: les petits flux concaténés, chacun aligné sur un mini secteur.
    ministream = bytearray()
    minifat = []
    for e in small:
        first = len(ministream) // MINISECTOR
        n = _ceil(len(e.data), MINISECTOR)
        ministream += e.data + b"\x00" * (n * MINISECTOR - len(e.data))
        for k in range(n):
            minifat.append(first + k + 1 if k < n - 1 else ENDOFCHAIN)
        e.start = first
        e.size = len(e.data)
    for e in streams:
        if len(e.data) == 0:
            e.start, e.size = ENDOFCHAIN, 0

    minifat_bytes = b"".join(struct.pack("<I", v) for v in minifat)
    if minifat_bytes:
        pad = -len(minifat_bytes) % SECTOR
        minifat_bytes += struct.pack("<I", FREESECT) * (pad // 4)

    dir_bytes = b"".join(_dir_entry(e) for e in entries)
    dir_bytes += b"\x00" * (-len(dir_bytes) % SECTOR)

    n_big = [_ceil(len(e.data), SECTOR) for e in big]
    n_mini = _ceil(len(ministream), SECTOR)
    n_minifat = len(minifat_bytes) // SECTOR
    n_dir = len(dir_bytes) // SECTOR
    base = sum(n_big) + n_mini + n_minifat + n_dir

    n_fat = 1
    while True:
        need = _ceil(base + n_fat, SECTOR // 4)
        if need == n_fat:
            break
        n_fat = need
    assert n_fat <= 109, "il faudrait des secteurs DIFAT"

    total = base + n_fat
    fat = [FREESECT] * total

    def chain(first, count):
        for k in range(count):
            fat[first + k] = first + k + 1 if k < count - 1 else ENDOFCHAIN

    cur = 0
    for e, n in zip(big, n_big):
        e.start, e.size = cur, len(e.data)
        chain(cur, n)
        cur += n
    mini_start = cur if n_mini else ENDOFCHAIN
    if n_mini:
        chain(cur, n_mini)
        cur += n_mini
    minifat_start = cur if n_minifat else ENDOFCHAIN
    if n_minifat:
        chain(cur, n_minifat)
        cur += n_minifat
    dir_start = cur
    chain(cur, n_dir)
    cur += n_dir
    fat_sectors = list(range(cur, cur + n_fat))
    for s in fat_sectors:
        fat[s] = FATSECT

    root.start, root.size = mini_start, len(ministream)
    # L'entrée racine a été sérialisée avant de connaître sa chaîne: on refait le répertoire.
    dir_bytes = b"".join(_dir_entry(e) for e in entries)
    dir_bytes += b"\x00" * (-len(dir_bytes) % SECTOR)

    fat_bytes = b"".join(struct.pack("<I", v) for v in fat)
    fat_bytes += struct.pack("<I", FREESECT) * ((-len(fat_bytes) % SECTOR) // 4)

    header = bytearray(SECTOR)
    header[0:8] = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
    struct.pack_into("<HHHHH", header, 24, 0x003E, 0x0003, 0xFFFE, 9, 6)
    struct.pack_into("<I", header, 44, n_fat)
    struct.pack_into("<I", header, 48, dir_start)
    struct.pack_into("<I", header, 56, CUTOFF)
    struct.pack_into("<I", header, 60, minifat_start)
    struct.pack_into("<I", header, 64, n_minifat)
    struct.pack_into("<I", header, 68, ENDOFCHAIN)
    struct.pack_into("<I", header, 72, 0)
    for i in range(109):
        struct.pack_into("<I", header, 76 + 4 * i,
                         fat_sectors[i] if i < n_fat else FREESECT)

    with open(path, "wb") as f:
        f.write(header)
        for e in big:
            f.write(e.data + b"\x00" * (-len(e.data) % SECTOR))
        if n_mini:
            f.write(bytes(ministream) + b"\x00" * (-len(ministream) % SECTOR))
        f.write(minifat_bytes)
        f.write(dir_bytes)
        f.write(fat_bytes)
    return path
