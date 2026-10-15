# Tuần 5 (14/10 – 20/10/2026): Môi trường mô phỏng và bài lab GPIO, nút nhấn, ngắt, Timer

Chưa có bo mạch (PCB và linh kiện về khoảng 3 tuần cuối kỳ) nên theo hướng dẫn của GVHD, tuần này
dựng môi trường biên dịch + mô phỏng và viết trước các bài lab của tuần 6 kế hoạch cũ.
Kế hoạch mới: [`docs/ke-hoach/ke-hoach-dieu-chinh.md`](../ke-hoach/ke-hoach-dieu-chinh.md).

## 1. Môi trường

| Công cụ | Phiên bản | Ghi chú |
|---------|-----------|---------|
| avr-gcc | 16.1.0 (Scoop: `scoop install avr-gcc`) | kèm avr-libc, avr-objcopy, avr-size |
| avrdude | dùng khi có bo | `make flash` / `build.ps1 -Flash` qua USBasp |
| Proteus 8 | phòng thực hành | Hướng dẫn: [`simulation/README.md`](../../simulation/README.md) |
| KiCad | 10.0.6 | Thiết kế mạch (tuần 3–4) |

Build:

```powershell
cd firmware
powershell -ExecutionPolicy Bypass -File build.ps1
```

`make` vẫn dùng được nếu repo nằm ở đường dẫn không dấu (make trên Windows lỗi với thư mục kiểu "Đồ án 2").

## 2. Bài lab đã viết

| Bài | Nội dung | Kỹ thuật | Flash (byte) |
|-----|----------|----------|-------------:|
| [`01_gpio_led`](../../firmware/labs/01_gpio_led/main.c) | Nháy 8 LED, LED chạy, đếm nhị phân | `DDRC`, `PORTC`, `_delay_ms` | 286 |
| [`02_button`](../../firmware/labs/02_button/main.c) | SW1 xoay LED, SW2 đảo LED | Đọc `PIND`, chống dội 20 ms, bắt cạnh nhấn | 230 |
| [`03_ext_interrupt`](../../firmware/labs/03_ext_interrupt/main.c) | INT0 tăng bộ đếm, INT1 xóa; PC7 nháy nền 1 Hz | `MCUCR` cạnh xuống, `GICR`, khóa ngắt 150 ms chống dội | 356 |
| [`04_timer`](../../firmware/labs/04_timer/main.c) | Timer1 CTC xuất 1 kHz ở OC1A; Timer0 tick 1 ms | CTC, so khớp đảo chân, ISR `TIMER0_COMP` | 384 |

Cả 4 bài biên dịch sạch với `-Wall -Wextra -Werror` (avr-gcc 16.1.0, `-Os`).

### Tính toán Timer (bài 04)

- Timer1, CTC, prescaler N = 8: `OCR1A = F_CPU / (2·N·f) − 1 = 8 000 000 / (2·8·1000) − 1 = 499`
  → OC1A đảo mỗi 0.5 ms → **f = 1000 Hz, chu kỳ 1 ms, duty 50 %**.
- Timer0, CTC, prescaler 64: `OCR0 = 8 000 000 / 64 / 1000 − 1 = 124` → ngắt mỗi **1.000 ms**.

## 3. Bảng kiểm thử trên mô phỏng

Cột "Kết quả" điền sau khi chạy trên Proteus (kèm ảnh trong `simulation/anh/`).

| # | Bài | Thao tác | Kết quả mong đợi | Kết quả | Ghi chú |
|--:|-----|----------|------------------|---------|---------|
| 1 | 01 | Run | 8 LED nháy cùng lúc 4 lần, chu kỳ 400 ms | | |
| 2 | 01 | Quan sát tiếp | LED sáng lần lượt PC0 → PC7, 2 vòng | | |
| 3 | 01 | Quan sát tiếp | LED đếm nhị phân 0 → 255, mỗi bước 50 ms | | |
| 4 | 02 | Nhấn SW1 1 lần | LED sáng dịch trái đúng 1 vị trí | | |
| 5 | 02 | Giữ SW1 | Không dịch thêm khi còn giữ | | |
| 6 | 02 | Nhấn SW2 | Toàn bộ LED đảo trạng thái | | |
| 7 | 03 | Nhấn SW1 n lần | PC0..PC6 hiển thị n (nhị phân) | | |
| 8 | 03 | Nhấn SW2 | Bộ đếm về 0 | | |
| 9 | 03 | Không nhấn | PC7 nháy 1 Hz đều | | |
| 10 | 04 | Counter Timer ở PD5 | 1.000 kHz | | |
| 11 | 04 | Oscilloscope ở PD5 | Xung vuông 5 V, chu kỳ 1 ms, duty 50 % | | |
| 12 | 04 | Quan sát LED | PC0 nháy 1 Hz, PC1 nháy 5 Hz, PC2..PC7 đếm giây | | |
| 13 | Tất cả | Để JTAGEN = Programmed | PC2..PC5 không hoạt động (kiểm chứng cần tắt JTAG) | | |

## 4. Nhật ký lỗi / vấn đề gặp phải

| Ngày | Vấn đề | Nguyên nhân | Cách khắc phục |
|------|--------|-------------|----------------|
| 15/10 | `make` báo "No targets specified" / "readdir: Invalid argument" | GNU make bản Windows không đọc được đường dẫn có dấu tiếng Việt | Viết thêm `build.ps1` (PowerShell) gọi trực tiếp avr-gcc |
