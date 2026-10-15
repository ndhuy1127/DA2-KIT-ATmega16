# Tuần 3 (30/09 – 06/10/2026): Vẽ schematic, gán footprint, chạy ERC

## 1. Kết quả

- Schematic KiCad: [`hardware/kicad/KIT-ATmega16.kicad_sch`](../../hardware/kicad/KIT-ATmega16.kicad_sch)
- Bản in PDF: [`hardware/output/KIT-ATmega16-schematic.pdf`](../../hardware/output/KIT-ATmega16-schematic.pdf)
- Báo cáo ERC: [`hardware/kicad/erc.rpt`](../../hardware/kicad/erc.rpt)
- Netlist: [`hardware/kicad/KIT-ATmega16.net`](../../hardware/kicad/KIT-ATmega16.net)

Toàn bộ mạch nằm trên một trang A3, chia theo khối: nguồn ở góc trên bên trái, reset và dao động ở bên
trái, MCU ở giữa, LED và nút nhấn bên phải, LCD và bàn phím ở mép phải, header mở rộng ở dưới.
Các đường tín hiệu nối với nhau bằng nhãn (net label) cho gọn, không kéo dây chéo qua trang.

## 2. Symbol và footprint

Tất cả lấy từ thư viện có sẵn của KiCad 10, không phải tự vẽ thêm:

| Linh kiện | Symbol | Footprint |
|-----------|--------|-----------|
| ATmega16A-PU | `MCU_Microchip_ATmega:ATmega16A-P` | `Package_DIP:DIP-40_W15.24mm_Socket` |
| LM7805 | `Regulator_Linear:L7805` | `Package_TO_SOT_THT:TO-220-3_Vertical` |
| Điện trở | `Device:R` | `R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` |
| Tụ gốm | `Device:C` | `C_Disc_D5.0mm_W2.5mm_P5.00mm` |
| Tụ hóa | `Device:C_Polarized` | `CP_Radial_D10.0mm_P5.00mm`, `CP_Radial_D6.3mm_P2.50mm` |
| Thạch anh | `Device:Crystal` | `Crystal_HC49-U_Vertical` |
| LED 3 mm | `Device:LED` | `LED_D3.0mm` |
| Nút nhấn | `Switch:SW_Push` | `SW_PUSH_6mm` |
| Biến trở | `Device:R_Potentiometer` | `Potentiometer_Bourns_3386P_Vertical` |
| Header ISP | `Conn_02x05_Odd_Even` | `IDC-Header_2x05_P2.54mm_Vertical` |
| LCD, bàn phím | `Conn_01x16`, `Conn_01x08` | `PinSocket_1x16`, `PinSocket_1x08` |

## 3. Đối chiếu với datasheet

| # | Hạng mục | Yêu cầu | Trên mạch | Đạt |
|--:|----------|---------|-----------|:---:|
| 1 | VCC, GND | VCC chân 10, GND chân 11 và 31 | Đúng, có C10 100 nF sát chân 10 | ✔ |
| 2 | AVCC | Nối VCC qua bộ lọc thông thấp khi dùng ADC | L1 10 µH và C8 100 nF | ✔ |
| 3 | AREF | Có tụ ra GND khi dùng AVCC làm tham chiếu | C9 100 nF | ✔ |
| 4 | RESET | Kéo lên 4,7–10 kΩ, tụ không quá 100 nF, diode về VCC (AN2519) | R2 10 kΩ, C5 100 nF, D3 1N4148 | ✔ |
| 5 | Thạch anh | Tụ 12–22 pF mỗi chân | 8 MHz, C6 và C7 22 pF | ✔ |
| 6 | ISP | MOSI = PB5, MISO = PB6, SCK = PB7, có RESET | J2: chân 1 MOSI, 5 RST, 7 SCK, 9 MISO, 4/6/8/10 GND | ✔ |
| 7 | LM7805 | Tụ vào từ 0,33 µF, tụ ra từ 0,1 µF | Vào 470 µF + 100 nF, ra 100 µF + 100 nF | ✔ |
| 8 | Chống ngược cực | Diode nối tiếp | D1 1N4007, sụt khoảng 0,7 V nên cần nguồn vào từ 8 V | ✔ |
| 9 | Dòng LED | Mỗi chân không quá 20 mA, tổng không quá 100 mA | (5 − 2) / 330 ≈ 9 mA, 8 LED ≈ 72 mA | ✔ |
| 10 | Nút INT0, INT1 | Có điện trở kéo lên, nhấn về GND | R11, R12 10 kΩ | ✔ |
| 11 | LCD | V0 qua biến trở, RW nối GND, đèn nền có điện trở hạn dòng | RV2, R13 33 Ω | ✔ |
| 12 | Bàn phím | 4 hàng là đầu ra, 4 cột là đầu vào có kéo lên | PB0–3 và PB4–7, dùng kéo lên nội | ✔ |
| 13 | UART | RXD nối TX của module, TXD nối RX, chung GND | J3: 1 GND, 2 PD0, 3 PD1 | ✔ |

## 4. Kiểm tra

- ERC trên KiCad 10.0.6 không còn lỗi hay cảnh báo nào.
- Đã so lại netlist với bảng phân chân tuần 2 (58 net, 208 chân), không thấy chỗ nào nối sai.
- Những chân không dùng (chân 3 của ISP, D0–D3 của LCD) đều được đánh dấu no-connect.
