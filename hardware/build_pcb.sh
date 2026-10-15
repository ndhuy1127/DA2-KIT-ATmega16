#!/bin/sh
# Đặt linh kiện -> Freerouting -> nhập SES + đổ đồng -> DRC -> xuất Gerber/Drill/ảnh.
# Biến môi trường: KICAD_BIN (thư mục bin của KiCad), JAVA (java >= 25), FREEROUTING (đường dẫn .jar)
set -e
cd "$(dirname "$0")"
KP="$KICAD_BIN/python.exe"; K="$KICAD_BIN/kicad-cli.exe"
PYTHONIOENCODING=utf-8 "$KP" scripts/gen_pcb.py place
"$JAVA" -jar "$FREEROUTING" -de kicad/KIT-ATmega16.dsn -do kicad/KIT-ATmega16.ses -mp 40 --gui.enabled=false > kicad/freerouting.log 2>&1
grep -E "0 unrouted|unrouted" kicad/freerouting.log | tail -1 || true
PYTHONIOENCODING=utf-8 "$KP" scripts/gen_pcb.py finish
"$K" pcb drc --severity-all --schematic-parity -o kicad/drc.rpt kicad/KIT-ATmega16.kicad_pcb
mkdir -p output/gerber
"$K" pcb export gerbers --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts -o output/gerber/ kicad/KIT-ATmega16.kicad_pcb
"$K" pcb export drill --format excellon --excellon-separate-th -o output/gerber/ kicad/KIT-ATmega16.kicad_pcb
python -I -c "import zipfile,glob,os; z=zipfile.ZipFile('output/KIT-ATmega16-gerber.zip','w',zipfile.ZIP_DEFLATED); [z.write(f,os.path.basename(f)) for f in sorted(glob.glob('output/gerber/*')) if f.endswith(('.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1','.drl','.gbrjob'))]"
"$K" sch export bom --fields "Reference,Value,Footprint,\${QUANTITY}" --group-by Value,Footprint -o output/bom.csv kicad/KIT-ATmega16.kicad_sch
"$K" pcb render --side top --width 1600 --height 1200 --quality high -o output/KIT-ATmega16-3d-top.png kicad/KIT-ATmega16.kicad_pcb
"$K" pcb render --side bottom --width 1600 --height 1200 -o output/KIT-ATmega16-3d-bottom.png kicad/KIT-ATmega16.kicad_pcb
"$K" pcb render --rotate "-45,0,30" --zoom 0.9 --width 1600 --height 1200 --quality high -o output/KIT-ATmega16-3d-iso.png kicad/KIT-ATmega16.kicad_pcb
"$K" pcb export pdf --mode-separate --layers F.Cu,B.Cu,F.Silkscreen,Edge.Cuts -o output/ kicad/KIT-ATmega16.kicad_pcb
