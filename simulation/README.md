# Mô phỏng KIT ATmega16 trên Proteus 8

Mạch mô phỏng dựng lại đúng phân chân của KIT thật (`docs/tuan-02/pinmap.md`) để file `.hex` chạy trên
mô phỏng cũng chạy được trên bo sau này mà không phải sửa code.

## 1. Linh kiện Proteus (Pick Devices)

| Khối KIT | Tên linh kiện Proteus | Nối với |
|----------|----------------------|---------|
| MCU | `ATMEGA16` | |
| 8 LED | `LED-RED` + `RES` 330 Ω | PC0..PC7 → R → LED → GND |
| SW1, SW2 | `BUTTON` + `RES` 10 kΩ kéo lên | PD2, PD3 (nhấn về GND) |
| Biến trở ADC | `POT-HG` 10 kΩ | 2 đầu: +5V/GND, con chạy: PA0 |
| LCD1602 | `LM016L` | RS = PD6, E = PD7, RW = GND, D4..D7 = PA4..PA7 |
| Keypad 4×4 | `KEYPAD-SMALLCALC` | Hàng A..D = PB0..PB3, cột 1..4 = PB4..PB7 |
| UART | `VIRTUAL TERMINAL` | RXD của terminal ← PD1 (TXD), TXD của terminal → PD0 (RXD); 9600 8N1 |
| Đo Timer | `OSCILLOSCOPE`, `COUNTER TIMER` (chế độ Frequency) | PD5 (OC1A) |

Không cần vẽ thạch anh, nguồn 7805, mạch reset: Proteus lấy clock từ thuộc tính MCU và cấp nguồn ngầm.

## 2. Thuộc tính ATMEGA16 (Edit Properties) — bắt buộc

| Thuộc tính | Giá trị | Tương ứng bo thật |
|------------|---------|-------------------|
| Program File | `firmware/build/<bài>.hex` | |
| CKSEL Fuses | `(1111) Ext. Crystal High Freq.` | LFUSE = 0xFF |
| Clock Frequency | `8MHz` | Thạch anh 8 MHz |
| JTAGEN | `(1) Unprogrammed` | HFUSE = 0xD9 |

> Nếu để JTAGEN mặc định (Programmed), LED PC2..PC5 sẽ không sáng — giống hệt hiện tượng trên bo thật khi
> chưa ghi fuse. Đây là lỗi nên ghi vào nhật ký nếu gặp.

## 3. Chạy mô phỏng

1. Build firmware: `cd firmware` rồi `powershell -ExecutionPolicy Bypass -File build.ps1`.
2. Mở mạch Proteus, chọn `Program File` là file `.hex` của bài cần thử.
3. Nhấn Run; quan sát LED / LCD / terminal, đo tần số bằng Counter Timer.
4. Ghi kết quả vào bảng trong `docs/tuan-05/mo-phong.md` (và ảnh chụp vào `simulation/anh/`).

Lưu file mạch Proteus vào thư mục này với tên `KIT-ATmega16.pdsprj`.

## 4. Phương án miễn phí: SimulIDE

SimulIDE (mã nguồn mở) có LED, nút, biến trở, LCD HD44780, keypad và serial monitor. Kiểm tra danh sách MCU
của phiên bản đang dùng có ATmega16 không; nếu không có thì dùng Proteus của phòng thực hành.
