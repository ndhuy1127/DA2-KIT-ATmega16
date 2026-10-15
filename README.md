# KIT phát triển ATmega16

Đồ án 2 – Học kỳ 20261 – Đại học Bách khoa Hà Nội

- **Mã lớp / mã đề tài:** 772645 / DA26111
- **Sinh viên thực hiện:** Nguyễn Đức Huy – 20233448
- **Giảng viên hướng dẫn:** ThS. Nguyễn Minh Đức

Đề tài thiết kế và lập trình một bo KIT dùng ATmega16. Trên bo có khối nguồn 5 V, thạch anh 8 MHz,
cổng nạp ISP cho USBasp, 8 LED đơn, 2 nút nhấn nối vào ngắt ngoài, biến trở để thử ADC, cổng UART,
chỗ cắm LCD1602 và bàn phím 4×4, cùng 4 header để đưa các cổng PORTA–PORTD ra ngoài.

![PCB 3D](hardware/output/KIT-ATmega16-3d-iso.png)

## Tiến độ

| Tuần | Nội dung | Tài liệu | Trạng thái |
|------|----------|----------|------------|
| 1 | Tìm hiểu yêu cầu, datasheet, sơ đồ khối | [tuan-01](docs/tuan-01/yeu-cau-va-so-do-khoi.md) | Xong |
| 2 | Phân chân, chọn linh kiện, BOM | [pinmap](docs/tuan-02/pinmap.md), [BOM](docs/tuan-02/bom.md) | Xong |
| 3 | Vẽ schematic, ERC | [tuan-03](docs/tuan-03/schematic.md), [PDF](hardware/output/KIT-ATmega16-schematic.pdf) | Xong |
| 4 | Vẽ PCB, DRC, xuất Gerber | [tuan-04](docs/tuan-04/pcb.md), [Gerber](hardware/output/KIT-ATmega16-gerber.zip) | Xong |
| 5 | Mô phỏng GPIO, nút nhấn, ngắt ngoài, Timer | [tuan-05](docs/tuan-05/mo-phong.md), [firmware](firmware/labs) | Đang làm |
| 6 | Mô phỏng ADC, UART | | |
| 7 | Mô phỏng LCD1602, bàn phím 4×4 | | |
| 8 | Bài tổng hợp, hàn lắp bo | | |
| 9 | Chạy trên bo thật, đo kiểm | | |
| 10 | Báo cáo, slide, demo | | |

Lịch chi tiết xem ở [docs/ke-hoach/ke-hoach-dieu-chinh.md](docs/ke-hoach/ke-hoach-dieu-chinh.md).

## Thư mục

```
docs/          kế hoạch, phiếu báo cáo tuần, tài liệu từng tuần
hardware/      project KiCad, file xuất (PDF, Gerber, BOM, ảnh 3D) và script hỗ trợ
firmware/      mã nguồn các bài lab, board.h chứa phân chân dùng chung
simulation/    mạch mô phỏng Proteus
```

## Build firmware

Trên Windows cài avr-gcc bằng Scoop (`scoop install avr-gcc`), sau đó:

```powershell
cd firmware
powershell -ExecutionPolicy Bypass -File build.ps1                       # build hết, ra build/*.hex
powershell -ExecutionPolicy Bypass -File build.ps1 -Lab 04_timer -Flash  # build và nạp 1 bài qua USBasp
```

Với chip mới cần ghi fuse một lần để chạy thạch anh 8 MHz và tắt JTAG:

```bash
avrdude -c usbasp -p m16 -U lfuse:w:0xFF:m -U hfuse:w:0xD9:m
```

## Phần cứng

Mở `hardware/kicad/KIT-ATmega16.kicad_pro` bằng KiCad 10. Schematic chạy ERC không còn lỗi;
PCB chạy DRC không còn lỗi và khớp với schematic, chỉ còn vài cảnh báo chữ silkscreen bị chồng.
