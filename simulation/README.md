# Mô phỏng KIT ATmega16 trên Proteus 8

Mạch mô phỏng nối đúng theo bảng phân chân của KIT (`docs/tuan-02/pinmap.md`), nhờ vậy file `.hex` chạy
được trên Proteus thì nạp vào bo thật cũng chạy y như vậy.

## 1. Linh kiện cần lấy trong Proteus

| Khối trên KIT | Tên trong Proteus | Cách nối |
|---------------|-------------------|----------|
| Vi điều khiển | `ATMEGA16` | |
| 8 LED | `LED-RED` và `RES` 330 Ω | PC0–PC7 → điện trở → LED → GND |
| SW1, SW2 | `BUTTON` và `RES` 10 kΩ kéo lên | PD2, PD3; bấm thì nối xuống GND |
| Biến trở ADC | `POT-HG` 10 kΩ | Hai đầu nối +5V và GND, con chạy nối PA0 |
| LCD1602 | `LM016L` | RS = PD6, E = PD7, RW = GND, D4–D7 = PA4–PA7 |
| Bàn phím 4×4 | `KEYPAD-SMALLCALC` | Hàng A–D = PB0–PB3, cột 1–4 = PB4–PB7 |
| UART | `VIRTUAL TERMINAL` | RXD của terminal nối PD1, TXD nối PD0; 9600 8N1 |
| Đo Timer | `OSCILLOSCOPE`, `COUNTER TIMER` (chế độ Frequency) | Nối vào PD5 (OC1A) |

Trên Proteus không cần vẽ thạch anh, khối nguồn 7805 hay mạch reset, vì clock lấy từ thuộc tính của chip
và nguồn được cấp sẵn.

## 2. Thuộc tính của ATMEGA16

Bấm đúp vào chip để mở Edit Properties và chỉnh:

| Thuộc tính | Giá trị | Tương ứng trên bo thật |
|------------|---------|------------------------|
| Program File | `firmware/build/<tên bài>.hex` | |
| CKSEL Fuses | `(1111) Ext. Crystal High Freq.` | LFUSE = 0xFF |
| Clock Frequency | `8MHz` | Thạch anh 8 MHz |
| JTAGEN | `(1) Unprogrammed` | HFUSE = 0xD9 |

JTAGEN mặc định đang là Programmed. Nếu không đổi thì 4 LED PC2–PC5 sẽ không sáng, giống hệt chuyện xảy ra
trên bo thật khi quên ghi fuse.

## 3. Các bước chạy

1. Build firmware: vào thư mục `firmware`, chạy `powershell -ExecutionPolicy Bypass -File build.ps1`.
2. Mở mạch Proteus, chọn Program File là file `.hex` của bài muốn thử.
3. Bấm Run, quan sát LED, LCD hoặc terminal; đo tần số bằng Counter Timer.
4. Ghi kết quả vào bảng trong `docs/tuan-05/mo-phong.md` và lưu ảnh chụp vào `simulation/anh/`.

File mạch Proteus lưu ở thư mục này với tên `KIT-ATmega16.pdsprj`.
