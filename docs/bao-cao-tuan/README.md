# Phiếu báo cáo tuần

- Tuần 1: [PhieuBaoCaoTuan1.docx](PhieuBaoCaoTuan1.docx)
- Tuần 2–5: nội dung bên dưới, chép sang mẫu phiếu Word khi nộp.

---

## Tuần 2 (23/09 – 29/09/2026) – Tiến độ tích lũy 20 %

**1. Công việc đã hoàn thành**
- Phân tích cách nối từng khối: nguồn, dao động, reset, ISP, LED, nút nhấn, ADC, UART, LCD, bàn phím.
- Lập bảng phân chân cho cả 40 chân ATmega16, chọn cấu hình fuse (LFUSE 0xFF, HFUSE 0xD9).
- Chọn linh kiện và footprint, hoàn thiện BOM, chia ra phần cần mua, phần mượn và phần có sẵn.

**2. Minh chứng:** `docs/tuan-02/pinmap.md`, `docs/tuan-02/bom.md` trên GitHub.

**3. Việc chưa hoàn thành:** Không có.

**4. Vướng mắc:** PB5–PB7 vừa nối bàn phím vừa là chân nạp ISP. Cách xử lý là không bấm phím trong lúc nạp.

**5. Kế hoạch tuần sau:** Vẽ schematic trên KiCad, gán footprint, chạy ERC và đối chiếu với datasheet.

---

## Tuần 3 (30/09 – 06/10/2026) – Tiến độ tích lũy 30 %

**1. Công việc đã hoàn thành**
- Vẽ xong schematic KIT trên KiCad 10, dùng thư viện có sẵn của KiCad.
- Gán footprint chân cắm cho tất cả linh kiện.
- Chạy ERC không còn lỗi; so netlist với bảng phân chân không thấy chỗ nối sai.
- Đối chiếu 13 hạng mục với datasheet ATmega16 và AN2519.

**2. Minh chứng:** `hardware/output/KIT-ATmega16-schematic.pdf`, `hardware/kicad/erc.rpt`, `docs/tuan-03/schematic.md`.

**3. Việc chưa hoàn thành:** Không có.

**4. Vướng mắc:** Không có.

**5. Kế hoạch tuần sau:** Bố trí linh kiện, đi dây PCB 2 lớp, chạy DRC, xuất Gerber và ảnh 3D.

---

## Tuần 4 (07/10 – 13/10/2026) – Tiến độ tích lũy 40 %

**1. Công việc đã hoàn thành**
- Bố trí linh kiện trên bo 150 × 110 mm theo từng khối chức năng.
- Đi dây 2 lớp (tín hiệu 0,4 mm, nguồn 0,8 mm), đổ đồng GND hai mặt.
- Chạy DRC không còn lỗi, PCB khớp với schematic; còn một số cảnh báo chữ silkscreen bị chồng.
- Xuất Gerber, file khoan, ảnh 3D và bản in từng lớp tỉ lệ 1:1.

**2. Minh chứng:** `hardware/output/` (file Gerber, ảnh 3D), `hardware/kicad/drc.rpt`, `docs/tuan-04/pcb.md`.

**3. Việc chưa hoàn thành:** Chưa gửi đặt mạch, đang chờ thầy xem layout.

**4. Vướng mắc / đề xuất:** Em nhờ thầy xem giúp layout trước khi đặt mạch.

**5. Kế hoạch tuần sau:** Dựng mạch mô phỏng, viết các bài GPIO, nút nhấn, ngắt ngoài, Timer.

---

## Tuần 5 (14/10 – 20/10/2026) – Tiến độ tích lũy 50 %

**1. Công việc đã hoàn thành**
- Cài avr-gcc, viết script build cho Windows.
- Dựng mạch mô phỏng Proteus nối đúng theo phân chân của KIT.
- Viết 4 bài: điều khiển LED, đọc nút nhấn có chống dội, ngắt ngoài INT0/INT1, Timer0/Timer1.
- Cập nhật lại lịch: làm firmware trên mô phỏng trước, hàn và đo bo ở tuần 8–9.

**2. Minh chứng:** `firmware/labs/01..04`, `docs/tuan-05/mo-phong.md`, ảnh mô phỏng trong `simulation/anh/`.

**3. Việc chưa hoàn thành:** Không có.

**4. Vướng mắc:** make trên Windows lỗi khi thư mục có dấu tiếng Việt, đã chuyển sang build bằng `build.ps1`.

**5. Kế hoạch tuần sau:** Bài ADC đọc biến trở và bài UART giao tiếp với Virtual Terminal trên mô phỏng.
