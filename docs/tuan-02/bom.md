# Danh mục vật tư (BOM) – KIT ATmega16

BOM xuất tự động từ schematic: [`hardware/output/bom.csv`](../../hardware/output/bom.csv).
Bảng dưới gom theo nhóm mua hàng; đơn giá là giá tham khảo cửa hàng linh kiện tại Hà Nội (tháng 9/2026).

## 1. Linh kiện trên bo

| STT | Ký hiệu | Linh kiện | Thông số | SL | Nguồn | Đơn giá (đ) | Thành tiền (đ) |
|---:|---|---|---|---:|---|---:|---:|
| 1 | U1 | ATmega16A-PU | AVR 8 bit, DIP-40 | 1 | Mua | 95.000 | 95.000 |
| 2 | (U1) | Đế IC DIP-40 | Tháo lắp MCU | 1 | Mua | 3.000 | 3.000 |
| 3 | U2 | LM7805 | TO-220, 5 V / 1 A | 1 | Mua | 5.000 | 5.000 |
| 4 | J1 | Jack DC | 5.5/2.1 mm, hàn xuyên lỗ | 1 | Mua | 3.000 | 3.000 |
| 5 | D1 | 1N4007 | Chống cắm ngược nguồn | 1 | Mua | 500 | 500 |
| 6 | D3 | 1N4148 | Kẹp xung trên RESET | 1 | Mua | 500 | 500 |
| 7 | C1 | Tụ hóa 470 µF / 25 V | Ø10 mm | 1 | Mua | 3.000 | 3.000 |
| 8 | C3 | Tụ hóa 100 µF / 16 V | Ø6.3 mm | 1 | Mua | 1.500 | 1.500 |
| 9 | C2, C4, C5, C8, C9, C10 | Tụ gốm 100 nF (104) | Bước chân 5 mm | 6 | Mua | 500 | 3.000 |
| 10 | C6, C7 | Tụ gốm 22 pF | Bước chân 5 mm | 2 | Mua | 500 | 1.000 |
| 11 | Y1 | Thạch anh 8 MHz | HC-49U | 1 | Mua | 3.000 | 3.000 |
| 12 | L1 | Cuộn cảm 10 µH | Dạng điện trở, lọc AVCC | 1 | Mua | 2.000 | 2.000 |
| 13 | R2, R11, R12 | Điện trở 10 kΩ | 1/4 W | 3 | Mua | 200 | 600 |
| 14 | R3–R10 | Điện trở 330 Ω | 1/4 W | 8 | Mua | 200 | 1.600 |
| 15 | R1 | Điện trở 1 kΩ | 1/4 W | 1 | Mua | 200 | 200 |
| 16 | R13 | Điện trở 33 Ω | 1/4 W, đèn nền LCD | 1 | Mua | 200 | 200 |
| 17 | D4–D11 | LED đỏ 3 mm | | 8 | Mua | 500 | 4.000 |
| 18 | D2 | LED xanh 3 mm | Báo nguồn | 1 | Mua | 500 | 500 |
| 19 | SW1–SW3 | Nút nhấn 6×6 mm | 4 chân | 3 | Mua | 1.000 | 3.000 |
| 20 | RV1, RV2 | Biến trở 10 kΩ | 3386P / 3296W | 2 | Mua | 4.000 | 8.000 |
| 21 | J2 | Header hộp IDC 2×5 | ISP USBasp | 1 | Mua | 3.000 | 3.000 |
| 22 | J4 | Header cái 1×16 | Cắm LCD1602 | 1 | Mua | 4.000 | 4.000 |
| 23 | J5 | Header cái 1×8 | Cắm keypad | 1 | Mua | 2.000 | 2.000 |
| 24 | J6–J9 | Header đực 1×10 | Mở rộng PORTA..D | 4 | Mua | 1.000 | 4.000 |
| 25 | J3, JP1 | Header đực 1×3, 1×2 + jumper | UART, chọn nguồn ISP | 1 bộ | Mua | 1.000 | 1.000 |

## 2. Module ngoài và dụng cụ

| STT | Linh kiện / module | Thông số | SL | Nguồn | Đơn giá (đ) | Thành tiền (đ) |
|---:|---|---|---:|---|---:|---:|
| 26 | LCD1602 | 16×2, 5 V, HD44780 | 1 | Mua mới / tự có | 45.000 | 45.000 |
| 27 | Ma trận phím 4×4 | 16 phím, 8 chân | 1 | Mua | 20.000 | 20.000 |
| 28 | USB-UART | CP2102 hoặc CH340 | 1 | Mua mới / tự có | 35.000 | 35.000 |
| 29 | Mạch nạp USBasp | ISP 10 chân | 1 | Đã có | 0 | 0 |
| 30 | Adapter 9 V / 1 A | Jack 5.5/2.1 mm | 1 | Tự có | 0 | 0 |
| 31 | PCB 2 lớp | 150 × 110 mm, đặt gia công | 2 bo | Đặt gia công | 80.000 | 160.000 |

**Tổng dự kiến:** 412.600 đ (linh kiện trên bo 152.600 đ, module 100.000 đ, PCB 160.000 đ) — sát ngân sách 412.000 đ trong kế hoạch.

## 3. Phân loại mua – mượn – tận dụng

- **Tự có / đã có:** USBasp, adapter 9 V, (có thể) LCD1602 và USB-UART.
- **Mượn phòng D8-705 nếu thiếu:** oscilloscope, nguồn DC giới hạn dòng, đồng hồ vạn năng, mỏ hàn.
- **Mua mới:** toàn bộ linh kiện nhóm 1, keypad 4×4.
- **Dự phòng:** mua thêm 1 ATmega16A, 1 LM7805, 2 thạch anh 8 MHz, 10 tụ 100 nF (linh kiện dễ hỏng khi hàn).

## 4. Thay đổi so với kế hoạch ban đầu

| Thay đổi | Lý do |
|----------|-------|
| Thêm L1 10 µH lọc AVCC | Theo AN2519 và datasheet mục ADC Noise Canceling |
| Thêm D3 1N4148 trên RESET | Theo AN2519, chống xung âm/ESD khi nhấn reset |
| Thêm 4 header 1×10 mở rộng cổng | Để nối dây thử nghiệm và đo tín hiệu |
| Header ISP dùng loại hộp IDC | Tránh cắm ngược cáp USBasp |
