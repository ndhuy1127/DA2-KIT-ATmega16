# Kế hoạch thực hiện (cập nhật từ tuần 5)

Từ tuần 5, phần firmware được làm trước và chạy thử trên mô phỏng Proteus. Phần hàn lắp và đo kiểm bo
chuyển xuống tuần 8–9, khi đó các bài lab đã chạy ổn trên mô phỏng nên chỉ việc nạp vào bo để kiểm tra.

| Tuần | Thời gian | Nội dung | Sản phẩm | Trạng thái |
|------|-----------|----------|----------|------------|
| 1 | 16/09 – 22/09 | Đọc yêu cầu, datasheet, lập sơ đồ khối | Sơ đồ khối, danh sách yêu cầu, tài liệu | Xong |
| 2 | 23/09 – 29/09 | Phân chân, chọn linh kiện, BOM | `docs/tuan-02` | Xong |
| 3 | 30/09 – 06/10 | Vẽ schematic, gán footprint, ERC | Schematic, báo cáo ERC | Xong |
| 4 | 07/10 – 13/10 | Vẽ PCB 2 lớp, DRC, xuất Gerber, ảnh 3D | PCB, báo cáo DRC, Gerber | Xong |
| 5 | 14/10 – 20/10 | Chuẩn bị môi trường mô phỏng; viết và chạy thử bài GPIO, nút nhấn, ngắt ngoài, Timer | `firmware/labs/01..04`, `simulation/` | Đang làm |
| 6 | 21/10 – 27/10 | Bài ADC đọc biến trở, bài UART giao tiếp với máy tính | `labs/05_adc`, `labs/06_uart`, log | |
| 7 | 28/10 – 03/11 | Bài LCD1602 và quét bàn phím 4×4 | `labs/07_lcd`, `labs/08_keypad` | |
| 8 | 04/11 – 10/11 | Bài tổng hợp; hàn bo theo từng khối, đo nguồn trước khi cắm MCU | `labs/09_tong_hop`, bảng đo VCC/AVCC/AREF | |
| 9 | 11/11 – 17/11 | Nạp ISP trên bo, chạy lại các bài lab, đo clock và tín hiệu bằng oscilloscope, sửa lỗi | Ảnh, video, bảng số liệu, nhật ký lỗi | |
| 10 | 18/11 – 24/11 | Hoàn thiện báo cáo, slide, kịch bản demo | Báo cáo PDF, slide, mã nguồn | |
