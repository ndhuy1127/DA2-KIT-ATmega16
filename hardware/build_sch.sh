#!/bin/sh
# Sinh lại schematic, nâng định dạng, kiểm tra ERC + netlist, xuất PDF.
set -e
cd "$(dirname "$0")"
K="$KICAD_BIN/kicad-cli.exe"
python -I scripts/gen_schematic.py
"$K" sch upgrade kicad/KIT-ATmega16.kicad_sch >/dev/null
"$K" sch erc --severity-all --exit-code-violations -o kicad/erc.rpt kicad/KIT-ATmega16.kicad_sch
"$K" sch export netlist -o kicad/KIT-ATmega16.net kicad/KIT-ATmega16.kicad_sch
python -I scripts/check_netlist.py
mkdir -p output
"$K" sch export pdf -o output/KIT-ATmega16-schematic.pdf kicad/KIT-ATmega16.kicad_sch
