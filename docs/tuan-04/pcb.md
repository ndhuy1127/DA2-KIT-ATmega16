# Tuần 4 (07/10 – 13/10/2026): Thiết kế PCB 2 lớp, DRC, xuất Gerber

![PCB 3D](../../hardware/output/KIT-ATmega16-3d-iso.png)

## 1. Sản phẩm

| File | Nội dung |
|------|----------|
| [`hardware/kicad/KIT-ATmega16.kicad_pcb`](../../hardware/kicad/KIT-ATmega16.kicad_pcb) | Layout PCB KiCad 10 |
| [`hardware/kicad/drc.rpt`](../../hardware/kicad/drc.rpt) | Báo cáo DRC (kèm kiểm tra khớp schematic) |
| [`hardware/output/KIT-ATmega16-gerber.zip`](../../hardware/output/KIT-ATmega16-gerber.zip) | Gerber + Drill gửi gia công |
| `hardware/output/KIT-ATmega16-3d-*.png` | Ảnh 3D mặt trên, mặt dưới, góc nghiêng |
| `hardware/output/KIT-ATmega16-{F_Cu,B_Cu,F_Silkscreen,Edge_Cuts}.pdf` | Bản in từng lớp (in 1:1 để ướm linh kiện) |

## 2. Thông số bo

| Thông số | Giá trị |
|----------|---------|
| Kích thước | 150 × 110 mm, 2 lớp, 4 lỗ bắt vít M3 ở góc |
| Linh kiện | 57 footprint, toàn bộ hàn xuyên lỗ (THT) |
| Đường mạch | Tín hiệu 0.4 mm; nguồn (+5V, GND, VIN, AVCC) 0.8 mm |
| Khoảng cách | Clearance 0.3 mm; cách mép bo 0.3 mm |
| Via | 1.0 / 0.5 mm (tín hiệu), 1.2 / 0.6 mm (nguồn) — 22 via |
| Đổ đồng | GND cả hai lớp, thermal relief cho pad (dễ hàn tay) |
| Tổng chiều dài dây | ≈ 5.6 m, 598 đoạn |

Các thông số đều nằm trong khả năng gia công phổ thông (JLCPCB/PCBWay: tối thiểu 0.127 mm / 0.3 mm khoan).

## 3. Bố trí linh kiện

- **Góc trên-trái – khối nguồn:** jack DC ở mép trái, 1N4007, tụ lọc, LM7805 (có chỗ trống phía trên để gắn tản nhiệt).
- **Giữa – MCU:** đế DIP-40; thạch anh và 2 tụ 22 pF đặt sát chân 12/13; C10 sát chân VCC;
  L1/C8/C9 sát chân AVCC/AREF.
- **Trái – reset & nạp:** nút RESET, R2/C5/D3, header ISP hộp IDC và jumper JP1, header UART ở mép trái.
- **Phải – ngoại vi:** dãy 8 LED + điện trở, biến trở ADC gần PA0, socket LCD1602, socket keypad 4×4.
- **Dưới – mở rộng:** 4 header PORTA..PORTD (mỗi header có thêm +5V, GND) và 2 nút SW1/SW2.

## 4. Quy trình và kết quả kiểm tra

1. Đặt linh kiện theo `PLACE` trong `hardware/scripts/gen_pcb.py`, gán net từ netlist schematic.
2. Đi dây tự động bằng **Freerouting 2.5.0** (DSN/SES): 0 kết nối chưa đi, 0 vi phạm.
3. Nhập lại vào KiCad, đổ đồng GND hai lớp.
4. **DRC KiCad 10.0.6 với `--schematic-parity`:**
   - **0 lỗi**, **0 kết nối hở**, **0 sai khác schematic–PCB**.
   - 17 cảnh báo silkscreen (chữ ký hiệu LED chồng viền LED bên cạnh, chữ H1/H2 sát mép bo):
     chỉ ảnh hưởng thẩm mỹ, sẽ chỉnh tay trong KiCad trước khi đặt mạch.

## 5. Việc cần làm trước khi đặt gia công

- [ ] Mở `KIT-ATmega16.kicad_pcb` trong KiCad, xem lại các đoạn dây tự động và chỉnh đẹp vùng quanh MCU.
- [ ] Dời chữ silkscreen bị chồng, chạy lại DRC.
- [ ] In 4 file PDF tỉ lệ 1:1, ướm thực tế LM7805, jack DC, biến trở, nút nhấn.
- [ ] Nhờ GVHD duyệt layout rồi mới gửi `KIT-ATmega16-gerber.zip`.

## 6. Cách sinh lại

```bash
export KICAD_BIN="/c/Users/<user>/AppData/Local/Programs/KiCad/10.0/bin"
export JAVA="<đường dẫn java 25>/bin/java.exe"
export FREEROUTING="<đường dẫn>/freerouting-2.5.0.jar"
sh hardware/build_pcb.sh
```

> Chạy lại sẽ đặt lại linh kiện và đi dây lại từ đầu (ghi đè chỉnh sửa tay). Sau khi đã chỉnh tay trong
> KiCad, chỉ dùng các lệnh `kicad-cli pcb drc / export` trong script.
