# Tuần 3 (30/09 – 06/10/2026): Vẽ mạch nguyên lý, gán footprint, ERC

## 1. Sản phẩm

| File | Nội dung |
|------|----------|
| [`hardware/kicad/KIT-ATmega16.kicad_sch`](../../hardware/kicad/KIT-ATmega16.kicad_sch) | Mạch nguyên lý KiCad 10 (1 trang A3) |
| [`hardware/output/KIT-ATmega16-schematic.pdf`](../../hardware/output/KIT-ATmega16-schematic.pdf) | Bản in PDF |
| [`hardware/kicad/erc.rpt`](../../hardware/kicad/erc.rpt) | Báo cáo ERC |
| [`hardware/kicad/KIT-ATmega16.net`](../../hardware/kicad/KIT-ATmega16.net) | Netlist |
| [`hardware/scripts/design.py`](../../hardware/scripts/design.py) | Bảng linh kiện – footprint – net (nguồn sinh schematic) |

Schematic được sinh từ `design.py` bằng script để bảng phân chân, firmware và mạch luôn thống nhất;
có thể mở và chỉnh trực tiếp bằng KiCad như file vẽ tay.

## 2. Thư viện và footprint

Toàn bộ symbol/footprint lấy từ thư viện chuẩn KiCad 10, không cần thư viện riêng:

| Linh kiện | Symbol | Footprint |
|-----------|--------|-----------|
| ATmega16A-PU | `MCU_Microchip_ATmega:ATmega16A-P` | `Package_DIP:DIP-40_W15.24mm_Socket` |
| LM7805 | `Regulator_Linear:L7805` | `Package_TO_SOT_THT:TO-220-3_Vertical` |
| Điện trở | `Device:R` | `R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` |
| Tụ gốm | `Device:C` | `C_Disc_D5.0mm_W2.5mm_P5.00mm` |
| Tụ hóa | `Device:C_Polarized` | `CP_Radial_D10.0mm_P5.00mm` / `CP_Radial_D6.3mm_P2.50mm` |
| Thạch anh | `Device:Crystal` | `Crystal_HC49-U_Vertical` |
| LED 3 mm | `Device:LED` | `LED_D3.0mm` |
| Nút nhấn | `Switch:SW_Push` | `SW_PUSH_6mm` |
| Biến trở | `Device:R_Potentiometer` | `Potentiometer_Bourns_3386P_Vertical` |
| ISP | `Conn_02x05_Odd_Even` | `IDC-Header_2x05_P2.54mm_Vertical` |
| LCD / keypad | `Conn_01x16` / `Conn_01x08` | `PinSocket_1x16` / `PinSocket_1x08` |

## 3. Checklist đối chiếu datasheet

| # | Hạng mục | Yêu cầu (nguồn) | Thiết kế | Kết quả |
|--:|----------|-----------------|----------|:------:|
| 1 | VCC/GND | Chân 10 VCC, 11 & 31 GND (datasheet – Pinout) | Đúng; C10 100 nF tại chân 10 | ✅ |
| 2 | AVCC | Nối VCC qua lọc thông thấp khi dùng ADC (datasheet – ADC) | L1 10 µH + C8 100 nF | ✅ |
| 3 | AREF | Tụ ngoài khi dùng AVCC làm tham chiếu | C9 100 nF xuống GND | ✅ |
| 4 | RESET | Kéo lên 4.7–10 kΩ, tụ ≤ 100 nF, diode về VCC (AN2519) | R2 10 kΩ, C5 100 nF, D3 1N4148 | ✅ |
| 5 | Thạch anh | 12–22 pF mỗi chân cho thạch anh (datasheet – Clock) | 8 MHz, C6/C7 22 pF | ✅ |
| 6 | ISP | MOSI=PB5, MISO=PB6, SCK=PB7, RESET (chuẩn 10 chân USBasp) | J2: 1 MOSI, 5 RST, 7 SCK, 9 MISO, 4/6/8/10 GND | ✅ |
| 7 | Nguồn | LM7805: tụ vào ≥ 0.33 µF, tụ ra ≥ 0.1 µF | C1 470 µF + C2 100 nF; C3 100 µF + C4 100 nF | ✅ |
| 8 | Chống ngược nguồn | Diode nối tiếp | D1 1N4007 (sụt ≈ 0.7 V, cần VIN ≥ 8 V) | ✅ |
| 9 | LED | I = (5 − 2) / 330 ≈ 9 mA < 20 mA/chân; tổng PORTC ≤ 100 mA (datasheet – DC char.) | 8 × 9 mA = 72 mA | ✅ |
| 10 | Nút INT0/INT1 | Có kéo lên, nhấn về GND | R11, R12 10 kΩ | ✅ |
| 11 | LCD | VSS, VDD, V0 qua biến trở, RW = GND, đèn nền có hạn dòng | RV2, R13 33 Ω | ✅ |
| 12 | Keypad | 4 hàng ra + 4 cột vào có kéo lên | PB0–3 / PB4–7 (kéo lên nội) | ✅ |
| 13 | UART | RXD (PD0) ← TX module, TXD (PD1) → RX module, chung GND | J3: 1 GND, 2 PD0, 3 PD1 | ✅ |

## 4. Kết quả kiểm tra

- **ERC (KiCad 10.0.6): 0 lỗi, 0 cảnh báo** — xem `hardware/kicad/erc.rpt`.
- **Netlist**: `scripts/check_netlist.py` so sánh netlist KiCad với bảng net thiết kế: 58 net / 208 chân,
  **0 sai lệch**.
- Các chân không dùng (ISP pin 3, LCD D0–D3) gắn cờ no-connect.

## 5. Cách sinh lại

```bash
export KICAD_BIN="/c/Users/<user>/AppData/Local/Programs/KiCad/10.0/bin"
sh hardware/build_sch.sh
```
