# Phần cứng KIT ATmega16

| Thư mục | Nội dung |
|---------|----------|
| `kicad/` | Project KiCad 10 (`KIT-ATmega16.kicad_pro`), báo cáo `erc.rpt`, `drc.rpt`, netlist |
| `output/` | Schematic PDF, Gerber zip, BOM, ảnh 3D, bản in từng lớp |
| `scripts/design.py` | Bảng linh kiện – footprint – net: nguồn dữ liệu của schematic |
| `scripts/gen_schematic.py` | Sinh `.kicad_sch` từ `design.py` |
| `scripts/check_netlist.py` | So netlist KiCad với `design.py` |
| `scripts/gen_pcb.py` | Đặt linh kiện, xuất DSN cho Freerouting, nhập SES, đổ đồng GND |

## Sinh lại

Yêu cầu: KiCad 10, Python 3, Java 25 và `freerouting-2.5.0.jar` (chỉ cần cho bước đi dây).

```bash
export KICAD_BIN="/c/Users/<user>/AppData/Local/Programs/KiCad/10.0/bin"
sh hardware/build_sch.sh      # schematic -> ERC -> netlist -> kiểm tra -> PDF

export JAVA="<java 25>/bin/java.exe"
export FREEROUTING="<đường dẫn>/freerouting-2.5.0.jar"
sh hardware/build_pcb.sh      # đặt linh kiện -> đi dây -> đổ đồng -> DRC -> Gerber, BOM, ảnh 3D
```

`build_pcb.sh` đặt và đi dây lại từ đầu, ghi đè mọi chỉnh sửa tay trên PCB. Sau khi đã chỉnh layout
trong KiCad, chỉ chạy các lệnh `kicad-cli pcb drc` / `export` tương ứng.
