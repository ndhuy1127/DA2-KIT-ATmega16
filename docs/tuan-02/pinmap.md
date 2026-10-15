# Tuần 2 (23/09 – 29/09/2026): Bảng phân chân và lựa chọn linh kiện

Bảng này là nguồn gốc của `firmware/common/board.h` và `hardware/scripts/design.py`.
Khi đổi phân chân phải sửa cả 3 nơi.

## 1. Bảng phân chân ATmega16A-PU (DIP-40)

| Chân | Tên | Chức năng trên KIT | Kết nối | Ghi chú |
|-----:|-----|--------------------|---------|---------|
| 1–4 | PB0–PB3 | Hàng phím R1–R4 | J5.1–4, J7 | Đầu ra khi quét phím |
| 5 | PB4 | Cột phím C1 | J5.5, J7 | Đầu vào, kéo lên nội |
| 6 | PB5 / MOSI | Cột phím C2 + ISP | J5.6, J2.1, J7 | Dùng chung với ISP |
| 7 | PB6 / MISO | Cột phím C3 + ISP | J5.7, J2.9, J7 | Dùng chung với ISP |
| 8 | PB7 / SCK | Cột phím C4 + ISP | J5.8, J2.7, J7 | Dùng chung với ISP |
| 9 | RESET | Reset | R2 10 kΩ, C5, SW3, D3, J2.5 | |
| 10 | VCC | +5 V | C10 100 nF sát chân | |
| 11, 31 | GND | Mass | | |
| 12 | XTAL2 | Thạch anh | Y1, C7 22 pF | |
| 13 | XTAL1 | Thạch anh | Y1, C6 22 pF | |
| 14 | PD0 / RXD | UART nhận | J3.2 (nối TX module), J9 | |
| 15 | PD1 / TXD | UART phát | J3.3 (nối RX module), J9 | |
| 16 | PD2 / INT0 | Nút SW1 | R11 10 kΩ kéo lên, J9 | Nhấn = 0 |
| 17 | PD3 / INT1 | Nút SW2 | R12 10 kΩ kéo lên, J9 | Nhấn = 0 |
| 18 | PD4 / OC1B | Tự do | J9 | Thử PWM |
| 19 | PD5 / OC1A | Đầu ra Timer1 | J9 | Đo tần số bằng oscilloscope |
| 20 | PD6 | LCD RS | J4.4, J9 | |
| 21 | PD7 | LCD EN | J4.6, J9 | |
| 22–29 | PC0–PC7 | 8 LED đơn | R3–R10 330 Ω → D4–D11 | Tích cực mức cao; **phải tắt JTAG** |
| 30 | AVCC | Nguồn analog | L1 10 µH từ +5 V, C8 100 nF | |
| 32 | AREF | Tham chiếu ADC | C9 100 nF xuống GND | Dùng tham chiếu AVCC |
| 33–36 | PA7–PA4 | LCD D7–D4 | J4.14–11, J6 | Chế độ 4 bit |
| 37–39 | PA3–PA1 | ADC3–ADC1 tự do | J6 | |
| 40 | PA0 / ADC0 | Biến trở RV1 | J6 | 0–5 V |

## 2. Lý do phân chân

- **LED trên PORTC**: cả cổng 8 bit liền nhau, ghi một lệnh `PORTC = x`. PC2–PC5 trùng JTAG nên fuse
  `JTAGEN` phải để 1 (tắt) — đã đưa vào `make fuses` (HFUSE = 0xD9).
- **Nút nhấn trên PD2/PD3**: đây là chân INT0/INT1 cứng, dùng chung cho bài polling và bài ngắt.
- **UART cố định ở PD0/PD1** (USART phần cứng).
- **LCD trên PA4–PA7 + PD6/PD7**: chừa PA0–PA3 cho ADC; RW nối GND (chỉ ghi) để tiết kiệm chân.
- **Keypad trên PORTB**: cần 8 chân liền nhau. PB5–PB7 dùng chung với ISP: khi nạp, MCU bị giữ reset nên các
  chân ở trạng thái tổng trở cao; chỉ cần **không nhấn phím trong lúc nạp**.
- **OC1A (PD5)** để trống cho bài Timer, có thể đo trực tiếp trên header J9.

## 3. Cấu hình fuse

| Fuse | Giá trị | Ý nghĩa |
|------|---------|---------|
| LFUSE | `0xFF` | CKSEL = 1111, SUT = 11: thạch anh ngoài 3–8 MHz, khởi động chậm |
| HFUSE | `0xD9` | JTAGEN = 1 (tắt JTAG), SPIEN = 0 (giữ nạp ISP), CKOPT = 1, BOOTRST = 1 |

> Mặc định xuất xưởng (LFUSE `0xE1`) chạy RC nội 1 MHz và bật JTAG; nếu chưa ghi fuse thì LED trên PC2–PC5
> không sáng và delay chậm gấp 8 lần.

## 4. Danh mục vật tư

Xem [bom.md](bom.md).
