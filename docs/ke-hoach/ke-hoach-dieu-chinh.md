# Kế hoạch điều chỉnh (từ tuần 5)

**Lý do:** theo ý kiến GVHD, PCB và linh kiện chỉ có trong khoảng 3 tuần cuối kỳ. Các việc hàn lắp, đo kiểm
phần cứng được dời xuống cuối; thời gian chờ dùng để tìm hiểu và **chạy mô phỏng** firmware trước
(đúng phương án dự phòng rủi ro số 1 trong kế hoạch: *"trong thời gian chờ tiếp tục viết code và kiểm tra
logic trên mô phỏng"*).

| Tuần | Thời gian | Nội dung | Sản phẩm | Trạng thái |
|------|-----------|----------|----------|:----------:|
| 1 | 16/09 – 22/09 | Đọc yêu cầu, datasheet, sơ đồ khối | Sơ đồ khối, danh sách yêu cầu, tài liệu | ✅ |
| 2 | 23/09 – 29/09 | Pin map, chọn linh kiện, BOM | `docs/tuan-02` | ✅ |
| 3 | 30/09 – 06/10 | Schematic, footprint, ERC | `hardware/kicad/*.kicad_sch`, ERC | ✅ |
| 4 | 07/10 – 13/10 | PCB 2 lớp, DRC, Gerber, 3D | `*.kicad_pcb`, DRC, Gerber | ✅ |
| **5** | **14/10 – 20/10** | **Dựng môi trường mô phỏng (Proteus/SimulIDE); viết và mô phỏng bài GPIO, nút nhấn, ngắt ngoài, Timer** | `firmware/labs/01..04`, `simulation/` | 🔄 đang làm |
| 6 | 21/10 – 27/10 | Mô phỏng ADC (biến trở) và UART (Virtual Terminal) | `labs/05_adc`, `labs/06_uart`, log | ⏳ |
| 7 | 28/10 – 03/11 | Mô phỏng LCD1602 và ma trận phím 4×4 | `labs/07_lcd`, `labs/08_keypad` | ⏳ |
| 8 | 04/11 – 10/11 | Bài tổng hợp trên mô phỏng; nhận PCB + linh kiện, hàn theo khối, đo nguồn trước khi lắp MCU | `labs/09_tong_hop`; bảng đo VCC/AVCC/AREF | ⏳ |
| 9 | 11/11 – 17/11 | Nạp ISP trên bo thật, chạy lại toàn bộ bài lab, đo clock/tín hiệu bằng oscilloscope, sửa lỗi | Ảnh/video, bảng số liệu, nhật ký lỗi | ⏳ |
| 10 | 18/11 – 24/11 | Hoàn thiện báo cáo, slide, kịch bản demo | Báo cáo PDF, slide, mã nguồn cuối kỳ | ⏳ |

Mốc phần cứng (hàn, kiểm tra chập, đo nguồn) của tuần 5 cũ được chuyển sang tuần 8–9.
