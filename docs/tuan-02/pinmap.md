# Tuần 2 (23/09 – 29/09/2026): Phân chân và chọn linh kiện

Bảng phân chân dưới đây cũng là nội dung của `firmware/common/board.h` và được dùng khi vẽ schematic.
Nếu sau này đổi chân nào thì phải sửa cả ba chỗ cho khớp.

## 1. Bảng phân chân ATmega16A-PU (DIP-40)

| Chân | Tên | Dùng cho | Nối tới | Ghi chú |
|-----:|-----|----------|---------|---------|
| 1–4 | PB0–PB3 | Hàng phím R1–R4 | J5.1–4, J7 | Là đầu ra khi quét phím |
| 5 | PB4 | Cột phím C1 | J5.5, J7 | Đầu vào, bật kéo lên nội |
| 6 | PB5 / MOSI | Cột phím C2, ISP | J5.6, J2.1, J7 | Dùng chung với ISP |
| 7 | PB6 / MISO | Cột phím C3, ISP | J5.7, J2.9, J7 | Dùng chung với ISP |
| 8 | PB7 / SCK | Cột phím C4, ISP | J5.8, J2.7, J7 | Dùng chung với ISP |
| 9 | RESET | Reset | R2, C5, SW3, D3, J2.5 | |
| 10 | VCC | +5 V | C10 100 nF đặt sát chân | |
| 11, 31 | GND | Mass | | |
| 12 | XTAL2 | Thạch anh | Y1, C7 22 pF | |
| 13 | XTAL1 | Thạch anh | Y1, C6 22 pF | |
| 14 | PD0 / RXD | UART nhận | J3.2 (nối chân TX của module), J9 | |
| 15 | PD1 / TXD | UART phát | J3.3 (nối chân RX của module), J9 | |
| 16 | PD2 / INT0 | Nút SW1 | R11 10 kΩ kéo lên, J9 | Nhấn thì về 0 |
| 17 | PD3 / INT1 | Nút SW2 | R12 10 kΩ kéo lên, J9 | Nhấn thì về 0 |
| 18 | PD4 / OC1B | Để trống | J9 | Có thể thử PWM |
| 19 | PD5 / OC1A | Ngõ ra Timer1 | J9 | Đo tần số bằng oscilloscope |
| 20 | PD6 | LCD RS | J4.4, J9 | |
| 21 | PD7 | LCD EN | J4.6, J9 | |
| 22–29 | PC0–PC7 | 8 LED đơn | R3–R10 330 Ω rồi tới D4–D11 | Sáng khi mức 1, cần tắt JTAG |
| 30 | AVCC | Nguồn analog | L1 10 µH từ +5 V, C8 100 nF | |
| 32 | AREF | Điện áp tham chiếu ADC | C9 100 nF xuống GND | Dùng tham chiếu AVCC |
| 33–36 | PA7–PA4 | LCD D7–D4 | J4.14–11, J6 | LCD chạy chế độ 4 bit |
| 37–39 | PA3–PA1 | ADC3–ADC1, để trống | J6 | |
| 40 | PA0 / ADC0 | Biến trở RV1 | J6 | 0–5 V |

## 2. Vì sao chia chân như vậy

- **LED để ở PORTC** vì đủ 8 bit liền nhau, ghi một lệnh `PORTC = x` là xong. Có điều PC2–PC5 trùng với
  JTAG nên phải tắt JTAG bằng fuse (HFUSE = 0xD9), nếu không bốn LED giữa sẽ không sáng.
- **Nút nhấn ở PD2 và PD3** vì đây là hai chân ngắt ngoài INT0, INT1. Bài đọc nút kiểu polling và bài
  ngắt dùng chung được hai nút này.
- **UART** bắt buộc ở PD0/PD1 vì đó là chân của USART phần cứng.
- **LCD dùng PA4–PA7 cùng PD6, PD7.** PA0–PA3 để dành cho ADC. Chân RW nối thẳng GND vì chỉ cần ghi ra LCD,
  đỡ tốn một chân.
- **Bàn phím ở PORTB** vì cần 8 chân. PB5–PB7 trùng với chân nạp ISP, nhưng lúc nạp chip bị giữ reset nên
  các chân này thả nổi, chỉ cần để ý đừng bấm phím trong lúc nạp.
- **PD5 (OC1A)** để trống cho bài Timer, đo trực tiếp được trên header J9.

## 3. Fuse

| Fuse | Giá trị | Ý nghĩa |
|------|---------|---------|
| LFUSE | `0xFF` | CKSEL = 1111, SUT = 11: thạch anh ngoài 3–8 MHz |
| HFUSE | `0xD9` | Tắt JTAG, giữ nguyên chế độ nạp ISP |

Chip mới mua mặc định chạy RC nội 1 MHz và bật JTAG. Nếu quên ghi fuse thì hàm delay chạy chậm gấp 8 lần
và LED PC2–PC5 không sáng.

## 4. Danh mục linh kiện

Xem [bom.md](bom.md).
