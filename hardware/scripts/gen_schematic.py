"""Sinh mạch nguyên lý KiCad (hardware/kicad/KIT-ATmega16.kicad_sch) từ design.py.

Chạy:  python hardware/scripts/gen_schematic.py
Sau đó: kicad-cli sch upgrade / erc / export netlist (xem hardware/README.md).
"""
import math
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))
sys.stdout.reconfigure(encoding="utf-8")
from sexpr import Sym, parse, dump, find, find_all  # noqa: E402
import design  # noqa: E402

KICAD_SHARE = os.environ.get('KICAD_SHARE', r'C:\Users\ndhuy\AppData\Local\Programs\KiCad\10.0\share\kicad')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'kicad')
PROJECT = 'KIT-ATmega16'
STUB = 2.54
NS = uuid.UUID('6f1c2a52-3c1e-4b8e-9a11-a16a16a16a16')
ROOT_UUID = str(uuid.uuid5(NS, 'root'))
POWER_NETS = ('+5V', 'GND')


def uid(*parts):
    return str(uuid.uuid5(NS, '/'.join(str(p) for p in parts)))


def S(x):
    return Sym(x)


# ------------------------------------------------------------ thư viện symbol
_lib_cache = {}


def load_lib(lib):
    if lib not in _lib_cache:
        path = os.path.join(KICAD_SHARE, 'symbols', lib + '.kicad_sym')
        tree = parse(open(path, encoding='utf-8').read())
        _lib_cache[lib] = {s[1]: s for s in find_all(tree, 'symbol')}
    return _lib_cache[lib]


def flat_symbol(lib_id):
    """Trả về symbol đã 'làm phẳng' (giải quyết extends) với tên lib_id."""
    lib, name = lib_id.split(':')
    syms = load_lib(lib)
    sym = syms[name]
    ext = find(sym, 'extends')
    if not ext:
        out = [x for x in sym]
        out[1] = lib_id
        return out
    base = flat_symbol(f'{lib}:{ext[1]}')
    base_name = ext[1]
    props = {p[1]: p for p in find_all(sym, 'property')}
    out = [S('symbol'), lib_id]
    for x in base[2:]:
        if isinstance(x, list) and x[0] == 'property' and x[1] in props:
            out.append(props.pop(x[1]))
        elif isinstance(x, list) and x[0] == 'symbol':
            unit = [y for y in x]
            unit[1] = unit[1].replace(base_name, name, 1)
            out.append(unit)
        else:
            out.append(x)
    # thuộc tính chỉ có ở symbol con
    insert_at = max(i for i, x in enumerate(out) if isinstance(x, list) and x[0] == 'property') + 1
    for p in props.values():
        out.insert(insert_at, p)
        insert_at += 1
    return out


def lib_pins(lib_id):
    """{số chân: (x, y, góc)} theo tọa độ symbol (y hướng lên)."""
    sym = flat_symbol(lib_id)
    pins = {}
    for unit in find_all(sym, 'symbol'):
        for p in find_all(unit, 'pin'):
            at = find(p, 'at')
            pins.setdefault(find(p, 'number')[1], (float(at[1]), float(at[2]), int(float(at[3]))))
    return pins


# ------------------------------------------------------------ hình học
def rot_pt(x, y, deg):
    r = math.radians(deg)
    return (x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r))


DIRS = {0: (-1, 0), 180: (1, 0), 90: (0, -1), 270: (0, 1)}   # hướng ra ngoài (hệ y-lên)


def pin_geom(comp, num, lpins):
    px, py, ang = lpins[num]
    rx, ry = rot_pt(px, py, comp['rot'])
    ang = (ang + comp['rot']) % 360
    ox, oy = DIRS[ang]
    X = round(comp['x'] + rx, 2)
    Y = round(comp['y'] - ry, 2)
    return (X, Y), (ox, -oy)          # hướng ra ngoài theo hệ màn hình (y-xuống)


def label_angle(d):
    return {(1, 0): 0, (0, -1): 90, (-1, 0): 180, (0, 1): 270}[d]


def power_rot(net, d):
    if net == '+5V':           # mũi tên mặc định hướng lên
        return {(0, -1): 0, (-1, 0): 90, (0, 1): 180, (1, 0): 270}[d]
    return {(0, 1): 0, (1, 0): 90, (0, -1): 180, (-1, 0): 270}[d]     # GND hướng xuống


# ------------------------------------------------------------ phần tử
def effects(justify=None, hide=False):
    e = [S('effects'), [S('font'), [S('size'), 1.27, 1.27]]]
    if justify:
        e.append([S('justify')] + [S(j) for j in justify.split()])
    if hide:
        e.append([S('hide'), S('yes')])
    return e


def prop(name, value, x, y, justify=None, hide=False):
    return [S('property'), name, value, [S('at'), x, y, 0], effects(justify, hide)]


def lib_field(lib_id, name, x, y, rot, value, hide=False):
    """Đặt trường Reference/Value theo vị trí mặc định trong thư viện (đã xoay theo symbol)."""
    p = next(p for p in find_all(flat_symbol(lib_id), 'property') if p[1] == name)
    at = find(p, 'at')
    fx, fy = rot_pt(float(at[1]), float(at[2]), rot)
    ang = int(float(at[3])) if len(at) > 3 else 0
    if rot in (90, 270):
        # symbol xoay đứng (LED): xếp Reference/Value chồng nhau bên phải thân
        dy = -1.27 if name == 'Reference' else 1.27
        node = prop(name, value, round(x + 2.54, 2), round(y + dy, 2), 'left', hide)
        node[3][3] = 0
        return node
    else:
        e = find(p, 'effects')
        just = ' '.join(str(j) for j in find(e, 'justify')[1:]) if e and find(e, 'justify') else None
    node = prop(name, value, round(x + fx, 2), round(y - fy, 2), just, hide)
    node[3][3] = ang
    return node


def symbol_instance(ref, lib_id, value, fp, x, y, rot, pin_nums, in_bom=True, desc=''):
    is_power = ref.startswith('#')
    node = [S('symbol'), [S('lib_id'), lib_id], [S('at'), x, y, rot], [S('unit'), 1],
            [S('exclude_from_sim'), S('no')], [S('in_bom'), S('no' if is_power else 'yes' if in_bom else 'no')],
            [S('on_board'), S('no' if is_power else 'yes')], [S('dnp'), S('no')],
            [S('uuid'), uid('sym', ref)],
            lib_field(lib_id, 'Reference', x, y, rot, ref, hide=is_power),
            lib_field(lib_id, 'Value', x, y, rot, value),
            prop('Footprint', fp, x, y, hide=True),
            prop('Datasheet', '', x, y, hide=True),
            prop('Description', desc, x, y, hide=True)]
    for n in pin_nums:
        node.append([S('pin'), n, [S('uuid'), uid('pin', ref, n)]])
    node.append([S('instances'), [S('project'), PROJECT,
                                  [S('path'), '/' + ROOT_UUID, [S('reference'), ref], [S('unit'), 1]]]])
    return node


def wire(a, b, key):
    return [S('wire'), [S('pts'), [S('xy'), a[0], a[1]], [S('xy'), b[0], b[1]]],
            [S('stroke'), [S('width'), 0], [S('type'), S('default')]], [S('uuid'), uid('wire', key)]]


def label(name, at, d, key):
    ang = label_angle(d)
    just = 'left bottom' if ang in (0, 90) else 'right bottom'
    return [S('label'), name, [S('at'), at[0], at[1], ang], [S('fields_autoplaced'), S('yes')],
            effects(just), [S('uuid'), uid('label', key)]]


def no_connect(at, key):
    return [S('no_connect'), [S('at'), at[0], at[1]], [S('uuid'), uid('nc', key)]]


# ------------------------------------------------------------ sinh file
def build():
    items, lib_ids = [], []
    points = {}              # tọa độ -> tên net (để phát hiện chạm chập ngoài ý muốn)
    direct = {}              # net '~' -> danh sách điểm chân
    pwr_count = 0

    def claim(pt, net, what):
        old = points.get(pt)
        if old is not None and old != net:
            raise SystemExit(f'Xung đột tại {pt}: {old} vs {net} ({what})')
        points[pt] = net

    for c in design.COMPONENTS:
        if c['lib'] not in lib_ids:
            lib_ids.append(c['lib'])
        lp = lib_pins(c['lib'])
        missing = set(lp) - set(c['pins'])
        if missing and c['pins']:
            raise SystemExit(f"{c['ref']}: thiếu khai báo chân {sorted(missing)}")
        items.append(symbol_instance(c['ref'], c['lib'], c['value'], c['fp'], c['x'], c['y'], c['rot'],
                                     sorted(lp, key=lambda s: int(s) if s.isdigit() else 0),
                                     in_bom=c['in_bom'], desc=c['desc']))
        for num, net in c['pins'].items():
            stub = STUB
            if isinstance(net, tuple):          # (tên net, chiều dài dây ra)
                net, stub = net
            (px, py), d = pin_geom(c, num, lp)
            key = f"{c['ref']}.{num}"
            if net is None:
                claim((px, py), '__nc_' + key, key)
                items.append(no_connect((px, py), key))
                continue
            claim((px, py), net, key)
            if net.startswith('~'):
                direct.setdefault(net, []).append((px, py))
                continue
            end = (round(px + d[0] * stub, 2), round(py + d[1] * stub, 2))
            # dây ngắn từ chân ra
            for k in range(1, int(round(stub / 1.27))):
                claim((round(px + d[0] * 1.27 * k, 2), round(py + d[1] * 1.27 * k, 2)), net, key)
            claim(end, net, key)
            items.append(wire((px, py), end, key))
            if net in POWER_NETS:
                pwr_count += 1
                ref = f'#PWR{pwr_count:03d}'
                lib_id = f'power:{net}'
                if lib_id not in lib_ids:
                    lib_ids.append(lib_id)
                items.append(symbol_instance(ref, lib_id, net, '', end[0], end[1], power_rot(net, d), ['1']))
            else:
                items.append(label(net, end, d, key))

    for net, pts in direct.items():
        if len(pts) < 2:
            raise SystemExit(f'Net {net} chỉ có 1 chân')
        pts.sort()
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            if a[0] != b[0] and a[1] != b[1]:
                corner = (b[0], a[1])
                items.append(wire(a, corner, f'{net}.{i}a'))
                items.append(wire(corner, b, f'{net}.{i}b'))
            else:
                items.append(wire(a, b, f'{net}.{i}'))

    lib_symbols = [S('lib_symbols')] + [flat_symbol(l) for l in lib_ids]
    sch = [S('kicad_sch'), [S('version'), 20231120], [S('generator'), 'eeschema'],
           [S('generator_version'), '8.0'], [S('uuid'), ROOT_UUID], [S('paper'), 'A3'],
           [S('title_block'), [S('title'), 'KIT phát triển ATmega16'], [S('date'), '2026-10-06'],
            [S('rev'), '1.0'], [S('company'), 'Đồ án 2 - DA26111 - Nguyễn Đức Huy'],
            [S('comment'), 1, 'GVHD: ThS. Nguyễn Minh Đức'],
            [S('comment'), 2, 'Sinh tự động bởi hardware/scripts/gen_schematic.py']],
           lib_symbols] + items + [
           [S('sheet_instances'), [S('path'), '/', [S('page'), '1']]]]
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, PROJECT + '.kicad_sch')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(dump(sch) + '\n')
    print('Đã ghi', os.path.normpath(out), f'({len(design.COMPONENTS)} linh kiện)')


if __name__ == '__main__':
    build()
