# Build toàn bộ bài lab cho ATmega16 @ 8 MHz
#   make                          -> build tất cả, file .hex nằm trong build/
#   make flash LAB=01_gpio_led    -> nạp 1 bài qua USBasp
#   make fuses                    -> ghi fuse: thạch anh ngoài 8 MHz, tắt JTAG

MCU      := atmega16
F_CPU    := 8000000UL
CC       := avr-gcc
OBJCOPY  := avr-objcopy
SIZE     := avr-size
AVRDUDE  := avrdude
PROG     := usbasp

CFLAGS   := -mmcu=$(MCU) -DF_CPU=$(F_CPU) -Os -std=gnu11 -Wall -Wextra -Werror \
            -ffunction-sections -fdata-sections -Icommon
LDFLAGS  := -Wl,--gc-sections

# Liệt kê tường minh (không dùng $(wildcard)): make bản Windows lỗi readdir khi
# đường dẫn thư mục có dấu tiếng Việt, ví dụ "D:/Đồ án 2/...".
LABS     := 01_gpio_led 02_button 03_ext_interrupt 04_timer
COMMON   :=
HEXES    := $(addprefix build/,$(addsuffix .hex,$(LABS)))

# Fuse ATmega16:
#   LFUSE 0xFF: CKSEL = 1111, SUT = 11 -> thạch anh ngoài 3..8 MHz, khởi động chậm
#   HFUSE 0xD9: OCDEN=1, JTAGEN=1 (tắt JTAG để dùng PC2..PC5), SPIEN=0 (giữ ISP),
#               CKOPT=1 (đủ cho thạch anh <= 8 MHz), EESAVE=1, BOOTSZ=00, BOOTRST=1
LFUSE    := 0xFF
HFUSE    := 0xD9

.PHONY: all clean flash fuses
.SECONDARY:

all: $(HEXES)

build/%.elf: labs/%/main.c $(COMMON) common/board.h | build
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(filter %.c,$^)
	$(SIZE) $@

build/%.hex: build/%.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

build:
	mkdir -p build

flash: build/$(LAB).hex
	$(AVRDUDE) -c $(PROG) -p m16 -U flash:w:$<:i

fuses:
	$(AVRDUDE) -c $(PROG) -p m16 -U lfuse:w:$(LFUSE):m -U hfuse:w:$(HFUSE):m

clean:
	rm -rf build
