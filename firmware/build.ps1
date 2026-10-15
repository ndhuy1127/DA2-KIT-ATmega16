# Build toàn bộ bài lab (Windows PowerShell). Dùng thay cho Makefile khi đường
# dẫn có dấu tiếng Việt (make bản Windows không đọc được thư mục như "Đồ án 2").
#
#   .\build.ps1                       -> build tất cả, .hex nằm trong build\
#   .\build.ps1 -Lab 04_timer         -> chỉ build 1 bài
#   .\build.ps1 -Lab 04_timer -Flash  -> build rồi nạp qua USBasp
param(
    [string]$Lab = "*",
    [switch]$Flash
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$mcu    = "atmega16"
$cflags = @("-mmcu=$mcu", "-DF_CPU=8000000UL", "-Os", "-std=gnu11", "-Wall", "-Wextra", "-Werror",
            "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections", "-Icommon")
$common = @(Get-ChildItem common -Filter *.c | ForEach-Object { $_.FullName })

New-Item -ItemType Directory -Force build | Out-Null

$labs = @(Get-ChildItem labs -Directory -Filter $Lab)
if ($labs.Count -eq 0) { throw "Không tìm thấy bài lab '$Lab'" }

foreach ($dir in $labs) {
    $name = $dir.Name
    $srcs = @(Get-ChildItem $dir.FullName -Filter *.c | ForEach-Object { $_.FullName }) + $common
    Write-Host "== $name" -ForegroundColor Cyan
    & avr-gcc @cflags -o "build\$name.elf" @srcs
    if ($LASTEXITCODE -ne 0) { throw "Biên dịch $name thất bại" }
    & avr-objcopy -O ihex -R .eeprom "build\$name.elf" "build\$name.hex"
    & avr-size "build\$name.elf"
}

if ($Flash) {
    if ($labs.Count -ne 1) { throw "Chỉ nạp được 1 bài, hãy chỉ định -Lab <tên>" }
    & avrdude -c usbasp -p m16 -U "flash:w:build\$($labs[0].Name).hex:i"
}
