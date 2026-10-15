# Tuần 5 (14/10 – 20/10/2026): Mô phỏng bài GPIO, nút nhấn, ngắt ngoài và Timer

Tuần này cài đặt công cụ biên dịch, dựng mạch mô phỏng trên Proteus theo đúng phân chân của KIT và viết
bốn bài lab đầu tiên. Vì mạch mô phỏng nối giống hệt bo thật nên file `.hex` chạy được trên mô phỏng cũng
nạp thẳng vào bo được, không phải sửa gì.

## 1. Công cụ

- **avr-gcc 16.1.0** (cài bằng `scoop install avr-gcc`), đi kèm avr-libc, avr-objcopy, avr-size.
- **avrdude** để nạp qua USBasp.
- **Proteus 8** để mô phỏng, cách dựng mạch ở [`simulation/README.md`](../../simulation/README.md).

Build tất cả các bài:

```powershell
cd firmware
powershell -ExecutionPolicy Bypass -File build.ps1
```

Ban đầu định dùng `make`, nhưng make trên Windows không đọc được thư mục có dấu như "Đồ án 2" nên viết thêm
file `build.ps1` chạy bằng PowerShell. Makefile vẫn để lại, dùng được khi đặt project ở đường dẫn không dấu.

## 2. Các bài lab

**[01_gpio_led](../../firmware/labs/01_gpio_led/main.c)** – Cho 8 LED nháy cùng lúc, chạy từ PC0 tới PC7,
rồi đếm nhị phân 0–255. Bài này để kiểm tra từng LED và từng chân của PORTC.

**[02_button](../../firmware/labs/02_button/main.c)** – Đọc nút bằng cách hỏi vòng. Bấm SW1 thì LED sáng
dịch sang trái một vị trí, bấm SW2 thì đảo toàn bộ LED. Có chống dội 20 ms và chỉ xử lý lúc vừa bấm xuống,
giữ nút thì không lặp lại.

**[03_ext_interrupt](../../firmware/labs/03_ext_interrupt/main.c)** – Dùng ngắt ngoài bắt cạnh xuống.
INT0 (SW1) tăng bộ đếm và hiện lên PC0–PC6, INT1 (SW2) xóa bộ đếm về 0. Trong lúc đó vòng lặp chính chỉ nháy
PC7 mỗi giây, để thấy rõ nút được xử lý bằng ngắt. Sau mỗi lần ngắt, chương trình khóa ngắt đó 150 ms để
tránh đếm nhiều lần do dội phím.

**[04_timer](../../firmware/labs/04_timer/main.c)** – Timer1 chạy chế độ CTC, tự đảo chân OC1A (PD5) để ra
xung vuông 1 kHz. Timer0 cũng chạy CTC, tạo ngắt mỗi 1 ms để làm bộ đếm thời gian; dùng nó cho PC0 nháy 1 Hz,
PC1 nháy 5 Hz và PC2–PC7 đếm số giây.

Cả bốn bài biên dịch không có cảnh báo với `-Wall -Wextra -Werror`. Kích thước sau khi build lần lượt là
286, 230, 356 và 384 byte.

### Tính thông số Timer

- Timer1, CTC, chia tần N = 8:
  `OCR1A = F_CPU / (2 · N · f) − 1 = 8 000 000 / (2 · 8 · 1000) − 1 = 499`.
  Chân OC1A đảo trạng thái mỗi 0,5 ms nên ra xung 1000 Hz, chu kỳ 1 ms, độ rộng xung 50 %.
- Timer0, CTC, chia tần 64: `OCR0 = 8 000 000 / 64 / 1000 − 1 = 124`, tức là cứ 1 ms ngắt một lần.

## 3. Kết quả chạy mô phỏng

| # | Bài | Thao tác | Kết quả mong đợi | Kết quả thực tế | Ghi chú |
|--:|-----|----------|------------------|-----------------|---------|
| 1 | 01 | Chạy mô phỏng | 8 LED nháy cùng lúc 4 lần, chu kỳ 400 ms | | |
| 2 | 01 | Quan sát tiếp | LED sáng lần lượt từ PC0 tới PC7, 2 vòng | | |
| 3 | 01 | Quan sát tiếp | LED đếm nhị phân 0 → 255, mỗi bước 50 ms | | |
| 4 | 02 | Bấm SW1 một lần | LED dịch trái đúng 1 vị trí | | |
| 5 | 02 | Giữ SW1 | Không dịch thêm khi còn giữ | | |
| 6 | 02 | Bấm SW2 | Tất cả LED đảo trạng thái | | |
| 7 | 03 | Bấm SW1 n lần | PC0–PC6 hiện số n dạng nhị phân | | |
| 8 | 03 | Bấm SW2 | Bộ đếm về 0 | | |
| 9 | 03 | Không bấm gì | PC7 nháy đều 1 Hz | | |
| 10 | 04 | Đo PD5 bằng Counter Timer | 1,000 kHz | | |
| 11 | 04 | Xem PD5 trên Oscilloscope | Xung vuông 5 V, chu kỳ 1 ms, độ rộng 50 % | | |
| 12 | 04 | Quan sát LED | PC0 nháy 1 Hz, PC1 nháy 5 Hz, PC2–PC7 đếm giây | | |
| 13 | Cả 4 bài | Để JTAGEN ở Programmed | PC2–PC5 không hoạt động, cho thấy phải tắt JTAG | | |

Ảnh chụp mô phỏng lưu trong `simulation/anh/`.

## 4. Lỗi gặp phải

| Ngày | Hiện tượng | Nguyên nhân | Cách xử lý |
|------|------------|-------------|------------|
| 15/10 | `make` báo "No targets specified" và "readdir: Invalid argument" | make trên Windows không đọc được đường dẫn có dấu tiếng Việt | Viết `build.ps1` gọi thẳng avr-gcc |
