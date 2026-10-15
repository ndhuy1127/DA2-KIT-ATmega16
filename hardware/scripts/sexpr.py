"""Bộ đọc/ghi S-expression tối giản cho file KiCad (.kicad_sym, .kicad_sch)."""
import re

_TOKEN = re.compile(r'\s*(?:(\()|(\))|("(?:[^"\\]|\\.)*")|([^\s()"]+))', re.S)


class Sym(str):
    """Ký hiệu không có dấu ngoặc kép (vd: symbol, at, yes)."""


def parse(text):
    stack, cur = [], []
    pos = 0
    while True:
        m = _TOKEN.match(text, pos)
        if not m or m.end() == pos:
            break
        pos = m.end()
        lp, rp, s, a = m.groups()
        if lp:
            stack.append(cur)
            cur = []
        elif rp:
            done = cur
            cur = stack.pop()
            cur.append(done)
        elif s is not None:
            cur.append(s[1:-1].replace('\\"', '"').replace('\\\\', '\\'))
        else:
            cur.append(Sym(a))
    return cur[0]


def dump(node, indent=0):
    if not isinstance(node, list):
        if isinstance(node, Sym):
            return str(node)
        if isinstance(node, (int, float)):
            return fmt_num(node)
        return '"' + str(node).replace('\\', '\\\\').replace('"', '\\"') + '"'
    simple = all(not isinstance(x, list) for x in node)
    if simple:
        return '(' + ' '.join(dump(x) for x in node) + ')'
    pad = '\t' * (indent + 1)
    parts = [dump(node[0])]
    out = '(' + parts[0]
    for x in node[1:]:
        if isinstance(x, list):
            out += '\n' + pad + dump(x, indent + 1)
        else:
            out += ' ' + dump(x)
    return out + '\n' + '\t' * indent + ')'


def fmt_num(v):
    if isinstance(v, int):
        return str(v)
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def find(node, key):
    for x in node:
        if isinstance(x, list) and x and x[0] == key:
            return x
    return None


def find_all(node, key):
    return [x for x in node if isinstance(x, list) and x and x[0] == key]
