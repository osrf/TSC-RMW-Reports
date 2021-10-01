import csv


def _key(db, key):
    key = str(key)
    if key not in db:
        db[key] = {}
    return db[key]


def key(db, *args):
    for arg in args:
        db = _key(db, arg)
    return db


def data(source):
    i = 0
    for j, line in enumerate(source):
        if line.startswith('---'):
            i = j
            break

    keys = [h.split("(")[0].strip('\n\t ') for h in source[j+1].split(',')]
    reader = csv.DictReader(source[j+2:], fieldnames=keys)
    rows = [row for row in reader]
    return keys, rows


def path(source):
    data = {}

    rmw = source[4].split(':')[1].strip().replace('rmw_', '').replace('_cpp', '')
    if 'cyclone' in source[3].split(':')[1].lower():
        rmw = 'raw_cyclonedds'

    reliable = 'RELIABLE' in source[6]
    transient = 'TRANSIENT' in source[6]
    rate = int(source[7].split(':')[1].strip())
    topic = source[8].split(':')[1].strip()
    subs = int(source[12].split(':')[1].strip())
    zero_copy = int(source[16].split(':')[1].strip()) > 0

    return [
        topic,
        rate,
        subs,
        zero_copy,
        reliable,
        transient,
        rmw
    ]


def collect_csv(file, db, host, mode):
    source = list(file.readlines())
    if len(source) < 25:
        return
    try:
        entry = key(db, host, mode, *path(source))
        header, values = data(source)
        for h in header:
            entry[h] = [row[h] for row in values]
    except:
        pass
