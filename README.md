# KIT phát triển ATmega16

Đồ án 2 – Học kỳ 20261 – Đại học Bách khoa Hà Nội

| | |
|---|---|
| Mã lớp / Mã đề tài | 772645 / DA26111 |
| Sinh viên | Nguyễn Đức Huy – 20233448 |
| GVHD | ThS. Nguyễn Minh Đức |

Thiết kế, chế tạo và lập trình một bo KIT ATmega16: nguồn 5 V, thạch anh 8 MHz, nạp ISP (USBasp),
8 LED, 2 nút nhấn ngắt ngoài, biến trở ADC, UART, LCD1602, ma trận phím 4×4 và 4 header mở rộng cổng.

![PCB 3D](hardware/output/KIT-ATmega16-3d-iso.png)

## Tiến độ

Kế hoạch đã điều chỉnh từ tuần 5 vì bo mạch chỉ có vào ~3 tuần cuối: firmware được làm trước trên mô phỏng,
hàn lắp và đo kiểm dời sang tuần 8–9. Chi tiết: [docs/ke-hoach/ke-hoach-dieu-chinh.md](docs/ke-hoach/ke-hoach-dieu-chinh.md).

| Tuần | Nội dung | Sản phẩm | |
|------|----------|----------|:-:|
| 1 | Yêu cầu, datasheet, sơ đồ khối | [docs/tuan-01](docs/tuan-01/yeu-cau-va-so-do-khoi.md) | ✅ |
| 2 | Pin map, BOM | [pinmap](docs/tuan-02/pinmap.md), [BOM](docs/tuan-02/bom.md) | ✅ |
| 3 | Schematic, ERC | [docs/tuan-03](docs/tuan-03/schematic.md), [PDF](hardware/output/KIT-ATmega16-schematic.pdf) | ✅ |
| 4 | PCB, DRC, Gerber | [docs/tuan-04](docs/tuan-04/pcb.md), [Gerber](hardware/output/KIT-ATmega16-gerber.zip) | ✅ |
| 5 | Mô phỏng: GPIO, nút, ngắt, Timer | [docs/tuan-05](docs/tuan-05/mo-phong.md), [firmware/labs](firmware/labs) | 🔄 |
| 6 | Mô phỏng: ADC, UART | | ⏳ |
| 7 | Mô phỏng: LCD1602, keypad 4×4 | | ⏳ |
| 8 | Bài tổng hợp; hàn lắp bo | | ⏳ |
| 9 | Nạp và chạy trên bo thật, đo kiểm | | ⏳ |
| 10 | Báo cáo, slide, demo | | ⏳ |

## Cấu trúc thư mục

```
docs/
  ke-hoach/        Kế hoạch gốc (.docx) và kế hoạch điều chỉnh
  bao-cao-tuan/    Phiếu báo cáo tuần
  tuan-01..05/     Tài liệu kỹ thuật từng tuần
hardware/
  kicad/           Project KiCad 10: schematic, PCB, báo cáo ERC/DRC, netlist
  output/          PDF schematic, Gerber zip, BOM, ảnh 3D, bản in từng lớp
  scripts/         Script sinh schematic/PCB và kiểm tra netlist
firmware/
  common/board.h   Phân chân và cấu hình chung
  labs/NN_ten/     Mỗi bài lab một thư mục
  build.ps1        Build trên Windows (PowerShell)
  Makefile         Build bằng make (đường dẫn không dấu / Linux)
simulation/        Hướng dẫn và file mô phỏng Proteus
```

## Build và nạp firmware

Cài toolchain (Windows, qua [Scoop](https://scoop.sh)): `scoop install avr-gcc` (avrdude cài thêm khi có bo).

```powershell
cd firmware
powershell -ExecutionPolicy Bypass -File build.ps1                    # build tất cả -> build/*.hex
powershell -ExecutionPolicy Bypass -File build.ps1 -Lab 04_timer -Flash  # build và nạp 1 bài qua USBasp
```

Lần đầu nạp chip mới phải ghi fuse (thạch anh 8 MHz, tắt JTAG):

```bash
avrdude -c usbasp -p m16 -U lfuse:w:0xFF:m -U hfuse:w:0xD9:m
```

## Phần cứng

Mở `hardware/kicad/KIT-ATmega16.kicad_pro` bằng KiCad 10. Kết quả kiểm tra hiện tại:

- ERC: 0 lỗi, 0 cảnh báo; netlist khớp bảng phân chân (58 net / 208 chân).
- DRC: 0 lỗi, 0 kết nối hở, PCB khớp schematic; 17 cảnh báo silkscreen.
