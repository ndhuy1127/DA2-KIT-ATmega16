# Phần cứng

- `kicad/` – project KiCad 10 (`KIT-ATmega16.kicad_pro`), báo cáo ERC, DRC và netlist.
- `output/` – schematic PDF, file Gerber nén, BOM, ảnh 3D và bản in từng lớp.
- `scripts/` – các script Python hỗ trợ:
  - `design.py`: danh sách linh kiện, footprint và cách nối dây.
  - `gen_schematic.py`: tạo file schematic từ `design.py`.
  - `check_netlist.py`: so netlist KiCad với `design.py` để bắt chỗ nối sai.
  - `gen_pcb.py`: đặt linh kiện lên PCB, trao đổi với Freerouting để đi dây, đổ đồng GND.

## Chạy lại các bước

Cần KiCad 10 và Python 3. Riêng bước đi dây cần thêm Java 25 và `freerouting-2.5.0.jar`.

```bash
export KICAD_BIN="/c/Users/<user>/AppData/Local/Programs/KiCad/10.0/bin"
sh hardware/build_sch.sh      # tạo schematic, chạy ERC, xuất netlist, kiểm tra, xuất PDF

export JAVA="<java 25>/bin/java.exe"
export FREEROUTING="<đường dẫn>/freerouting-2.5.0.jar"
sh hardware/build_pcb.sh      # đặt linh kiện, đi dây, đổ đồng, chạy DRC, xuất Gerber, BOM, ảnh 3D
```

Lưu ý: `build_pcb.sh` đặt và đi dây lại từ đầu, nên sẽ ghi đè những gì đã chỉnh tay trên PCB. Khi đã sửa
layout trong KiCad thì chỉ chạy riêng các lệnh `kicad-cli pcb drc` và `export`.
