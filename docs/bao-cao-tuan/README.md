# Phiếu báo cáo tuần

| Tuần | File | Ghi chú |
|------|------|---------|
| 1 | [PhieuBaoCaoTuan1.docx](PhieuBaoCaoTuan1.docx) | Đã nộp |
| 2–5 | Bản nháp bên dưới | Chép vào mẫu phiếu Word; số giờ làm việc, ngày báo cáo tự điền |

---

## Tuần 2 (23/09 – 29/09/2026) — tiến độ tích lũy 20 %

**1. Công việc đã hoàn thành**
- Phân tích kết nối từng khối (nguồn, clock, reset, ISP, LED, nút, ADC, UART, LCD, keypad).
- Lập bảng phân chân I/O cho 40 chân ATmega16, xác định cấu hình fuse (LFUSE 0xFF, HFUSE 0xD9).
- Chọn linh kiện, footprint; hoàn thiện BOM và phân loại mua – mượn – tận dụng.

**2. Minh chứng:** `docs/tuan-02/pinmap.md`, `docs/tuan-02/bom.md` trên GitHub.

**3. Việc chưa hoàn thành:** Không.

**4. Vướng mắc:** PB5–PB7 vừa dùng cho keypad vừa dùng cho ISP — giải pháp: không nhấn phím khi nạp.

**5. Kế hoạch tuần sau:** Vẽ schematic trên KiCad, gán footprint, chạy ERC, checklist đối chiếu datasheet.

---

## Tuần 3 (30/09 – 06/10/2026) — tiến độ tích lũy 30 %

**1. Công việc đã hoàn thành**
- Vẽ mạch nguyên lý KIT trên KiCad 10 (60 symbol, 58 net), dùng thư viện chuẩn KiCad.
- Gán footprint THT cho toàn bộ linh kiện.
- Chạy ERC: 0 lỗi, 0 cảnh báo. Đối chiếu netlist với bảng phân chân: 0 sai lệch.
- Lập checklist 13 mục đối chiếu datasheet ATmega16 / AN2519.

**2. Minh chứng:** `hardware/output/KIT-ATmega16-schematic.pdf`, `hardware/kicad/erc.rpt`, `docs/tuan-03/schematic.md`.

**3. Việc chưa hoàn thành:** Không.

**4. Vướng mắc:** Không.

**5. Kế hoạch tuần sau:** Bố trí linh kiện, đi dây PCB 2 lớp, DRC, xuất Gerber và ảnh 3D.

---

## Tuần 4 (07/10 – 13/10/2026) — tiến độ tích lũy 40 %

**1. Công việc đã hoàn thành**
- Bố trí 57 footprint trên bo 150 × 110 mm theo khối chức năng.
- Đi dây 2 lớp (tín hiệu 0.4 mm, nguồn 0.8 mm), đổ đồng GND hai mặt.
- DRC: 0 lỗi, 0 kết nối hở, PCB khớp schematic; còn 17 cảnh báo silkscreen sẽ chỉnh tay.
- Xuất Gerber/Drill, ảnh 3D, bản in từng lớp tỉ lệ 1:1.

**2. Minh chứng:** `hardware/output/` (Gerber zip, ảnh 3D), `hardware/kicad/drc.rpt`, `docs/tuan-04/pcb.md`.

**3. Việc chưa hoàn thành:** Chưa đặt gia công PCB — chờ GVHD duyệt layout.

**4. Vướng mắc / đề xuất:** Đề nghị thầy xem giúp layout trước khi đặt mạch.

**5. Kế hoạch tuần sau:** Hàn lắp theo khối (theo kế hoạch ban đầu).

---

## Tuần 5 (14/10 – 20/10/2026) — tiến độ tích lũy 50 %

**1. Công việc đã hoàn thành**
- Theo hướng dẫn GVHD (bo và linh kiện về khoảng 3 tuần cuối): điều chỉnh kế hoạch, dời hàn lắp sang tuần 8–9,
  chuyển phần firmware lên trước và kiểm thử bằng mô phỏng.
- Cài môi trường avr-gcc, viết script build; lập hướng dẫn dựng mạch mô phỏng Proteus theo đúng phân chân KIT.
- Viết 4 bài lab: GPIO LED, nút nhấn (polling + chống dội), ngắt ngoài INT0/INT1, Timer0/Timer1.

**2. Minh chứng:** `firmware/labs/01..04`, `docs/tuan-05/mo-phong.md`, `docs/ke-hoach/ke-hoach-dieu-chinh.md`;
ảnh chạy mô phỏng (bổ sung vào `simulation/anh/` sau khi chạy Proteus).

**3. Việc chưa hoàn thành:** Hàn lắp, đo nguồn — dời sang tuần 8–9 do chưa có bo.

**4. Vướng mắc:** GNU make trên Windows lỗi với đường dẫn có dấu → đã viết `build.ps1` thay thế.

**5. Kế hoạch tuần sau:** Bài ADC (đọc biến trở) và UART (trao đổi với Virtual Terminal) trên mô phỏng.
