"""Dữ liệu thiết kế KIT ATmega16: linh kiện, footprint, vị trí trên schematic và net.

Đây là nguồn dữ liệu duy nhất của mạch nguyên lý. gen_schematic.py đọc file này
để sinh hardware/kicad/KIT-ATmega16.kicad_sch; check_netlist.py so sánh netlist
KiCad xuất ra với bảng net ở đây.

Quy ước net:
  "+5V", "GND"      -> vẽ bằng power symbol
  "~TEN"            -> nối bằng dây trực tiếp giữa các chân (các chân phải thẳng hàng)
  None              -> chân bỏ trống, đặt cờ no-connect
  tên khác          -> nối bằng nhãn (label) cùng tên
Tọa độ schematic tính bằng mm, gốc ở góc trên-trái, y hướng xuống.
"""

FP = {
    'R': 'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',
    'C': 'Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm',
    'CP10': 'Capacitor_THT:CP_Radial_D10.0mm_P5.00mm',
    'CP6': 'Capacitor_THT:CP_Radial_D6.3mm_P2.50mm',
    'LED': 'LED_THT:LED_D3.0mm',
    'POT': 'Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical',
    'SW': 'Button_Switch_THT:SW_PUSH_6mm',
    'H10': 'Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical',
}

COMPONENTS = []


def add(ref, lib, value, fp, x, y, pins, rot=0, desc='', in_bom=True):
    COMPONENTS.append(dict(ref=ref, lib=lib, value=value, fp=fp, x=x, y=y,
                           rot=rot, pins=pins, desc=desc, in_bom=in_bom))


# ---------------------------------------------------------------- Khối nguồn
add('J1', 'Connector:Barrel_Jack', 'DC 9-12V', 'Connector_BarrelJack:BarrelJack_Horizontal',
    30.48, 45.72, {'1': '~VJACK', '2': 'GND'}, desc='Jack nguồn DC 5.5/2.1 mm')
add('D1', 'Diode:1N4007', '1N4007', 'Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal',
    55.88, 43.18, {'1': 'VIN', '2': '~VJACK'}, rot=180, desc='Chống cắm ngược cực')
add('C1', 'Device:C_Polarized', '470uF/25V', FP['CP10'], 76.2, 50.8, {'1': 'VIN', '2': 'GND'})
add('C2', 'Device:C', '100nF', FP['C'], 88.9, 50.8, {'1': 'VIN', '2': 'GND'})
add('U2', 'Regulator_Linear:L7805', 'LM7805', 'Package_TO_SOT_THT:TO-220-3_Vertical',
    109.22, 45.72, {'1': 'VIN', '2': 'GND', '3': '+5V'}, desc='Ổn áp 5 V')
add('C3', 'Device:C_Polarized', '100uF/16V', FP['CP6'], 129.54, 50.8, {'1': '+5V', '2': 'GND'})
add('C4', 'Device:C', '100nF', FP['C'], 142.24, 50.8, {'1': '+5V', '2': 'GND'})
add('R1', 'Device:R', '1k', FP['R'], 157.48, 45.72, {'1': '+5V', '2': '~LED_PWR'})
add('D2', 'Device:LED', 'Xanh', FP['LED'], 157.48, 58.42, {'2': '~LED_PWR', '1': 'GND'}, rot=90)
add('#FLG01', 'power:PWR_FLAG', 'PWR_FLAG', '', 66.04, 25.4, {'1': 'VIN'})
add('#FLG02', 'power:PWR_FLAG', 'PWR_FLAG', '', 78.74, 25.4, {'1': 'GND'})
add('#FLG03', 'power:PWR_FLAG', 'PWR_FLAG', '', 91.44, 25.4, {'1': 'AVCC'})

# ------------------------------------------------------ Reset, clock, AVCC
add('R2', 'Device:R', '10k', FP['R'], 35.56, 101.6, {'1': '+5V', '2': 'RESET'})
add('C5', 'Device:C', '100nF', FP['C'], 48.26, 104.14, {'1': 'RESET', '2': 'GND'})
add('SW3', 'Switch:SW_Push', 'RESET', FP['SW'], 66.04, 109.22, {'1': 'RESET', '2': 'GND'})
add('D3', 'Diode:1N4148', '1N4148', 'Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal',
    66.04, 91.44, {'1': '+5V', '2': 'RESET'}, desc='Kẹp xung ESD trên RESET (AN2519)')
add('Y1', 'Device:Crystal', '8MHz', 'Crystal:Crystal_HC49-U_Vertical',
    43.18, 142.24, {'1': 'XTAL1', '2': 'XTAL2'})
add('C6', 'Device:C', '22pF', FP['C'], 33.02, 157.48, {'1': 'XTAL1', '2': 'GND'})
add('C7', 'Device:C', '22pF', FP['C'], 53.34, 157.48, {'1': 'XTAL2', '2': 'GND'})
add('L1', 'Device:L', '10uH', 'Inductor_THT:L_Axial_L5.3mm_D2.2mm_P10.16mm_Horizontal_Vishay_IM-1',
    81.28, 142.24, {'1': '+5V', '2': 'AVCC'}, desc='Lọc nguồn analog (AN2519)')
add('C8', 'Device:C', '100nF', FP['C'], 93.98, 142.24, {'1': 'AVCC', '2': 'GND'})
add('C9', 'Device:C', '100nF', FP['C'], 106.68, 142.24, {'1': 'AREF', '2': 'GND'})
add('C10', 'Device:C', '100nF', FP['C'], 119.38, 142.24, {'1': '+5V', '2': 'GND'}, desc='Tụ thoát VCC sát chân 10')

# ------------------------------------------------------------------- MCU
MCU_PINS = {'9': 'RESET', '10': '+5V', '11': 'GND', '31': 'GND', '12': 'XTAL2', '13': 'XTAL1',
            '30': ('AVCC', 7.62), '32': 'AREF'}
for i in range(8):
    MCU_PINS[str(40 - i)] = f'PA{i}'
    MCU_PINS[str(1 + i)] = f'PB{i}'
    MCU_PINS[str(22 + i)] = f'PC{i}'
    MCU_PINS[str(14 + i)] = f'PD{i}'
add('U1', 'MCU_Microchip_ATmega:ATmega16A-P', 'ATmega16A-PU', 'Package_DIP:DIP-40_W15.24mm_Socket',
    203.2, 152.4, MCU_PINS)

# ------------------------------------------------------------ ISP, UART
add('J2', 'Connector_Generic:Conn_02x05_Odd_Even', 'ISP (USBasp)', 'Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical',
    45.72, 190.5, {'1': 'PB5', '2': 'ISP_VCC', '3': None, '4': 'GND', '5': 'RESET',
                   '6': 'GND', '7': 'PB7', '8': 'GND', '9': 'PB6', '10': 'GND'})
add('JP1', 'Connector_Generic:Conn_01x02', 'Cấp 5V từ ISP', 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
    86.36, 187.96, {'1': 'ISP_VCC', '2': '+5V'})
add('J3', 'Connector_Generic:Conn_01x03', 'USB-UART', 'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',
    86.36, 210.82, {'1': 'GND', '2': 'PD0', '3': 'PD1'}, desc='Pin2 RXD <- TX module; Pin3 TXD -> RX module')

# ------------------------------------------------------ LED đơn PORTC
for i in range(8):
    x = 271.78 + 12.7 * i
    add(f'R{3 + i}', 'Device:R', '330', FP['R'], x, 45.72, {'1': f'PC{i}', '2': f'~LED{i}'})
    add(f'D{4 + i}', 'Device:LED', 'Đỏ', FP['LED'], x, 58.42, {'2': f'~LED{i}', '1': 'GND'}, rot=90)

# ---------------------------------------------------- Nút nhấn INT0/INT1
add('R11', 'Device:R', '10k', FP['R'], 274.32, 88.9, {'1': '+5V', '2': 'PD2'})
add('SW1', 'Switch:SW_Push', 'SW1 (INT0)', FP['SW'], 297.18, 101.6, {'1': 'PD2', '2': 'GND'})
add('R12', 'Device:R', '10k', FP['R'], 320.04, 88.9, {'1': '+5V', '2': 'PD3'})
add('SW2', 'Switch:SW_Push', 'SW2 (INT1)', FP['SW'], 342.9, 101.6, {'1': 'PD3', '2': 'GND'})

# ------------------------------------------------------------- LCD1602
LCD = {'1': 'GND', '2': ('+5V', 7.62), '3': 'LCD_V0', '4': 'PD6', '5': 'GND', '6': 'PD7',
       '7': None, '8': None, '9': None, '10': None,
       '11': 'PA4', '12': 'PA5', '13': 'PA6', '14': 'PA7', '15': 'LCD_BL', '16': 'GND'}
add('J4', 'Connector_Generic:Conn_01x16', 'LCD1602', 'Connector_PinSocket_2.54mm:PinSocket_1x16_P2.54mm_Vertical',
    383.54, 147.32, LCD, desc='Chế độ 4 bit, RW nối GND')
add('RV2', 'Device:R_Potentiometer', '10k', FP['POT'], 325.12, 142.24,
    {'1': '+5V', '2': 'LCD_V0', '3': 'GND'}, desc='Chỉnh độ tương phản LCD')
add('R13', 'Device:R', '33', FP['R'], 345.44, 142.24, {'1': '+5V', '2': 'LCD_BL'}, desc='Hạn dòng đèn nền')

# -------------------------------------------------- Ma trận phím, ADC
KEY = {str(i + 1): f'PB{i}' for i in range(8)}
add('J5', 'Connector_Generic:Conn_01x08', 'Keypad 4x4', 'Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical',
    383.54, 200.66, KEY, desc='Pin1..4 = hàng R1..R4, pin5..8 = cột C1..C4')
add('RV1', 'Device:R_Potentiometer', '10k', FP['POT'], 325.12, 195.58,
    {'1': '+5V', '2': 'PA0', '3': 'GND'}, desc='Biến trở thử ADC0')

# ------------------------------------------------- Header mở rộng cổng
for k, port in enumerate('ABCD'):
    pins = {str(i + 1): f'P{port}{i}' for i in range(8)}
    pins.update({'9': '+5V', '10': 'GND'})
    add(f'J{6 + k}', 'Connector_Generic:Conn_01x10', f'PORT{port}', FP['H10'],
        154.94 + 45.72 * k, 248.92, pins)

# ------------------------------------------------------------ Lỗ bắt vít
for k in range(4):
    add(f'H{k + 1}', 'Mechanical:MountingHole', 'M3', 'MountingHole:MountingHole_3.2mm_M3',
        22.86 + 10.16 * k, 274.32, {}, in_bom=False)
