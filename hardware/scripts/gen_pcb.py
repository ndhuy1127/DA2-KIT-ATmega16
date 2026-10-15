"""Sinh PCB KiCad từ netlist schematic, xuất DSN để Freerouting đi dây, nhập SES và đổ đồng GND.

Chạy bằng Python đi kèm KiCad (có module pcbnew):
  <KiCad>/bin/python.exe hardware/scripts/gen_pcb.py place     # đặt linh kiện -> .kicad_pcb + .dsn
  java -jar freerouting.jar -de ... -do ...                  # đi dây tự động (xem hardware/README.md)
  <KiCad>/bin/python.exe hardware/scripts/gen_pcb.py finish    # nhập .ses, đổ đồng GND, lưu
"""
import os
import sys

import pcbnew

sys.path.insert(0, os.path.dirname(__file__))
from sexpr import parse, find, find_all  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
KDIR = os.path.normpath(os.path.join(HERE, '..', 'kicad'))
NETLIST = os.path.join(KDIR, 'KIT-ATmega16.net')
PCB = os.path.join(KDIR, 'KIT-ATmega16.kicad_pcb')
DSN = os.path.join(KDIR, 'KIT-ATmega16.dsn')
SES = os.path.join(KDIR, 'KIT-ATmega16.ses')
FP_DIR = os.environ.get('KICAD_FOOTPRINTS',
                        r'C:\Users\ndhuy\AppData\Local\Programs\KiCad\10.0\share\kicad\footprints')

OX, OY = 100.0, 50.0           # gốc bo trên trang
W, H = 150.0, 110.0            # kích thước bo (mm)
# tên net theo netlist KiCad (nhãn cục bộ có tiền tố '/')
POWER_NETS = ('+5V', 'GND', '/VIN', 'Net-(D1-A)', '/AVCC', '/ISP_VCC')

# ref: (x, y, góc) tính theo mm từ góc trên-trái của bo
PLACE = {
    # nguồn
    'J1': (14, 14, 0), 'D1': (22, 22, 0), 'C1': (36, 12, 0), 'C2': (48, 14, 0),
    'U2': (58, 12, 0), 'C3': (70, 12, 0), 'C4': (78, 14, 0),
    'R1': (122, 8, 0), 'D2': (137, 8, 0),
    # MCU và lân cận
    'U1': (62, 32, 0),
    'C10': (56, 58, 90), 'Y1': (50, 66, 90), 'C6': (44, 72, 90), 'C7': (44, 63, 90),
    'R2': (38, 52, 90), 'C5': (44, 52, 90), 'D3': (32, 52, 90), 'SW3': (12, 42, 0),
    'L1': (84, 58, 0), 'C8': (84, 62, 0), 'C9': (84, 52, 0), 'RV1': (88, 30, 0),
    # nạp / giao tiếp
    'J2': (22, 58, 0), 'JP1': (34, 62, 0), 'J3': (6, 84, 0),
    # nút nhấn
    'SW1': (14, 88, 0), 'SW2': (28, 88, 0), 'R11': (38, 80, 0), 'R12': (38, 84, 0),
    # LCD, phím
    'J4': (100, 70, 90), 'RV2': (96, 80, 0), 'R13': (110, 80, 0), 'J5': (118, 90, 90),
    # header cổng
    'J6': (12, 104, 90), 'J7': (46, 104, 90), 'J8': (80, 104, 90), 'J9': (114, 104, 90),
    # lỗ bắt vít
    'H1': (4, 4, 0), 'H2': (146, 4, 0), 'H3': (4, 106, 0), 'H4': (146, 106, 0),
}
for i in range(8):
    PLACE[f'R{3 + i}'] = (100 + 5.08 * i, 50, 90)
    PLACE[f'D{4 + i}'] = (100 + 5.08 * i, 33, 90)


def mm(v):
    return pcbnew.FromMM(v)


def pt(x, y):
    return pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))


def field(comp, name):
    for f in find_all(find(comp, 'fields'), 'field'):
        if find(f, 'name')[1] == name:
            return f[2] if len(f) > 2 else ''
    return ''


def read_netlist():
    tree = parse(open(NETLIST, encoding='utf-8').read())
    comps = []
    for c in find_all(find(tree, 'components'), 'comp'):
        comps.append(dict(ref=find(c, 'ref')[1], value=find(c, 'value')[1],
                          fp=find(c, 'footprint')[1], uuid=find(c, 'tstamps')[1],
                          desc=field(c, 'Description')))
    nets = {}
    for n in find_all(find(tree, 'nets'), 'net'):
        name = find(n, 'name')[1]
        for node in find_all(n, 'node'):
            nets[(find(node, 'ref')[1], find(node, 'pin')[1])] = name
    return comps, nets


def setup_rules(board):
    ds = board.GetDesignSettings()
    ns = ds.m_NetSettings
    default = ns.GetDefaultNetclass()
    default.SetClearance(mm(0.3))
    default.SetTrackWidth(mm(0.4))
    default.SetViaDiameter(mm(1.0))
    default.SetViaDrill(mm(0.5))
    power = pcbnew.NETCLASS('Power')
    power.SetClearance(mm(0.3))
    power.SetTrackWidth(mm(0.8))
    power.SetViaDiameter(mm(1.2))
    power.SetViaDrill(mm(0.6))
    ns.SetNetclass('Power', power)
    for net in POWER_NETS:
        ns.SetNetclassPatternAssignment(net, 'Power')
    ds.m_MinClearance = mm(0.2)
    ds.m_TrackMinWidth = mm(0.25)
    ds.m_CopperEdgeClearance = mm(0.3)


def edge(board):
    corners = [(0, 0), (W, 0), (W, H), (0, H)]
    for a, b in zip(corners, corners[1:] + corners[:1]):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pt(*a))
        s.SetEnd(pt(*b))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(mm(0.1))
        board.Add(s)


def silk_text(board, text, x, y, size=1.5):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(pt(x, y))
    t.SetLayer(pcbnew.F_SilkS)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(size * 0.15))
    board.Add(t)


def place():
    comps, pin_nets = read_netlist()
    board = pcbnew.NewBoard(PCB)
    setup_rules(board)

    netinfo = {}
    for name in sorted(set(pin_nets.values())):
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        netinfo[name] = ni

    for c in comps:
        lib, name = c['fp'].split(':')
        fp = pcbnew.FootprintLoad(os.path.join(FP_DIR, lib + '.pretty'), name)
        if fp is None:
            raise SystemExit(f"Không tìm thấy footprint {c['fp']}")
        fp.SetFPID(pcbnew.LIB_ID(lib, name))
        fp.SetReference(c['ref'])
        fp.SetValue(c['value'])
        fp.SetPath(pcbnew.KIID_PATH('/' + c['uuid']))
        fp.GetField(pcbnew.FIELD_T_DESCRIPTION).SetText(c['desc'])
        x, y, rot = PLACE[c['ref']]
        board.Add(fp)
        fp.SetPosition(pt(x, y))
        fp.SetOrientationDegrees(rot)
        for pad in fp.Pads():
            net = pin_nets.get((c['ref'], pad.GetNumber()))
            if net:
                pad.SetNet(netinfo[net])

    edge(board)
    silk_text(board, 'KIT ATmega16 - DA26111', 75, 92, 2.0)
    silk_text(board, 'Nguyen Duc Huy - 20233448 - HUST 2026', 75, 96, 1.2)
    board.Save(PCB)
    pcbnew.ExportSpecctraDSN(board, DSN)
    print('Đã ghi', PCB, 'và', DSN)


def gnd_zone(board, layer):
    gnd = board.FindNet('GND')
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(gnd)
    z.SetLocalClearance(mm(0.4))
    z.SetMinThickness(mm(0.3))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    z.SetThermalReliefGap(mm(0.5))
    z.SetThermalReliefSpokeWidth(mm(0.5))
    ol = z.Outline()
    ol.NewOutline()
    m = 0.5
    for x, y in [(m, m), (W - m, m), (W - m, H - m), (m, H - m)]:
        ol.Append(mm(OX + x), mm(OY + y))
    board.Add(z)


# Pad GND bị kẹp giữa các đường mạch, thermal relief chỉ ra được 1 nan -> nối đặc vào vùng đồng
SOLID_PADS = [('C8', '2'), ('J7', '10')]


def finish():
    board = pcbnew.LoadBoard(PCB)
    for ref, num in SOLID_PADS:
        for pad in board.FindFootprintByReference(ref).Pads():
            if pad.GetNumber() == num:
                pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    if not pcbnew.ImportSpecctraSES(board, SES):
        raise SystemExit('Nhập SES thất bại')
    gnd_zone(board, pcbnew.F_Cu)
    gnd_zone(board, pcbnew.B_Cu)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    board.Save(PCB)
    print('Đã nhập', SES, 'và đổ đồng GND')


if __name__ == '__main__':
    {'place': place, 'finish': finish}[sys.argv[1]]()
