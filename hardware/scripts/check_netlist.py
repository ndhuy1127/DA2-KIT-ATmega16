"""So sánh netlist KiCad xuất từ schematic với bảng net trong design.py.

Chạy:  kicad-cli sch export netlist -o hardware/kicad/KIT-ATmega16.net hardware/kicad/KIT-ATmega16.kicad_sch
       python hardware/scripts/check_netlist.py
Mỗi nhóm chân cùng net trong design.py phải là đúng một net trong netlist và ngược lại.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.stdout.reconfigure(encoding='utf-8')
from sexpr import parse, find, find_all  # noqa: E402
import design  # noqa: E402

NET = os.path.join(os.path.dirname(__file__), '..', 'kicad', 'KIT-ATmega16.net')


def main():
    tree = parse(open(NET, encoding='utf-8').read())
    actual = {}
    for net in find_all(find(tree, 'nets'), 'net'):
        name = find(net, 'name')[1]
        nodes = frozenset(f"{find(n, 'ref')[1]}.{find(n, 'pin')[1]}" for n in find_all(net, 'node'))
        actual[nodes] = name

    expected = {}
    for c in design.COMPONENTS:
        if c['ref'].startswith('#'):
            continue
        for pin, net in c['pins'].items():
            if isinstance(net, tuple):
                net = net[0]
            key = net if net is not None else f"__nc_{c['ref']}.{pin}"
            expected.setdefault(key, set()).add(f"{c['ref']}.{pin}")

    errors = 0
    seen = set()
    for net, nodes in sorted(expected.items()):
        nodes = frozenset(nodes)
        if nodes in actual:
            seen.add(nodes)
            continue
        errors += 1
        print(f'SAI: net {net} mong đợi {sorted(nodes)}')
        for a, name in actual.items():
            if a & nodes:
                print(f'     netlist có {name}: {sorted(a)}')
    for a, name in actual.items():
        if a not in seen:
            errors += 1
            print(f'THỪA: net {name} {sorted(a)}')

    total = sum(len(n) for n in expected.values())
    print(f'{len(expected)} net / {total} chân được kiểm tra, {errors} sai lệch')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
