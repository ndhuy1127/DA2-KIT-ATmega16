/*
 * board.h - Bảng phân chân (pin map) KIT ATmega16
 *
 * Nguồn gốc: docs/tuan-02/pinmap.md. Mọi thay đổi phân chân phải sửa đồng thời
 * ở file này, ở pinmap.md và ở schematic (hardware/kicad).
 *
 * Clock: thạch anh ngoài 8 MHz (fuse CKSEL = 1111, SUT = 11).
 * JTAG phải tắt (fuse JTAGEN = 1) để dùng PC2..PC5 làm GPIO cho LED.
 */
#ifndef BOARD_H
#define BOARD_H

#ifndef F_CPU
#define F_CPU 8000000UL
#endif

#include <avr/io.h>

/* ---- LED đơn: 8 LED nối PORTC, tích cực mức cao (qua R 330 Ω xuống GND) ---- */
#define LED_DDR        DDRC
#define LED_PORT       PORTC

/* ---- Nút nhấn: kéo lên 10 kΩ, nhấn = mức 0 ---- */
#define BTN_DDR        DDRD
#define BTN_PORT       PORTD
#define BTN_PIN        PIND
#define BTN1_BIT       PD2     /* SW1 -> INT0 */
#define BTN2_BIT       PD3     /* SW2 -> INT1 */

/* ---- Timer/Counter: chân so sánh ra để quan sát bằng oscilloscope ---- */
#define OC1A_DDR       DDRD
#define OC1A_BIT       PD5     /* OC1A */
#define OC0_DDR        DDRB
#define OC0_BIT        PB3     /* OC0 (dùng chung hàng phím ROW3, chỉ dùng khi không gắn phím) */

/* ---- ADC: biến trở VR1 nối ADC0 (PA0), tham chiếu AVCC ---- */
#define ADC_POT_CH     0

/* ---- UART: PD0 = RXD, PD1 = TXD -> module USB-UART (CP2102/CH340) ---- */
#define UART_BAUD      9600UL

/* ---- LCD1602 chế độ 4 bit: D4..D7 = PA4..PA7, RS = PD6, EN = PD7, RW nối GND ---- */
#define LCD_DATA_DDR   DDRA
#define LCD_DATA_PORT  PORTA
#define LCD_D4_BIT     PA4
#define LCD_CTRL_DDR   DDRD
#define LCD_CTRL_PORT  PORTD
#define LCD_RS_BIT     PD6
#define LCD_EN_BIT     PD7

/* ---- Ma trận phím 4x4: hàng PB0..PB3 (ra), cột PB4..PB7 (vào, kéo lên nội) ---- */
#define KEY_DDR        DDRB
#define KEY_PORT       PORTB
#define KEY_PIN        PINB
#define KEY_ROW_MASK   0x0F
#define KEY_COL_MASK   0xF0

#endif /* BOARD_H */
