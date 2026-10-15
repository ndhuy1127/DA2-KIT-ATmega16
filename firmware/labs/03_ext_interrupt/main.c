/*
 * Bài 03 - Ngắt ngoài INT0 / INT1
 *
 *   INT0 (PD2, SW1): cạnh xuống -> tăng bộ đếm, hiển thị nhị phân trên PC0..PC6
 *   INT1 (PD3, SW2): cạnh xuống -> xóa bộ đếm về 0
 *
 * Vòng lặp chính chỉ làm việc "nền" (nháy PC7 chu kỳ 1 s) để chứng minh
 * sự kiện nút nhấn được xử lý bởi ngắt chứ không phải hỏi vòng.
 * Chống dội: sau mỗi lần ngắt, tạm khóa ngắt đó trong LOCKOUT_MS (đếm trong
 * vòng lặp chính) để không đếm nhiều lần do dội phím.
 */
#include "board.h"
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdint.h>

#define LOCKOUT_MS 150
#define TICK_MS    10

static volatile uint8_t counter;
static volatile uint8_t lock0, lock1;     /* số tick còn khóa ngắt */

ISR(INT0_vect)
{
    counter++;
    GICR &= ~(1 << INT0);
    lock0 = LOCKOUT_MS / TICK_MS;
}

ISR(INT1_vect)
{
    counter = 0;
    GICR &= ~(1 << INT1);
    lock1 = LOCKOUT_MS / TICK_MS;
}

static void ext_int_init(void)
{
    BTN_DDR &= ~((1 << BTN1_BIT) | (1 << BTN2_BIT));
    BTN_PORT |= (1 << BTN1_BIT) | (1 << BTN2_BIT);

    /* ISCx1:ISCx0 = 10 -> ngắt khi có cạnh xuống */
    MCUCR = (MCUCR & 0xF0) | (1 << ISC01) | (1 << ISC11);
    GIFR = (1 << INTF0) | (1 << INTF1);   /* xóa cờ treo */
    GICR |= (1 << INT0) | (1 << INT1);
}

/* Mở lại ngắt sau thời gian khóa; xóa cờ phát sinh do dội trong lúc khóa.
 * Gọi khi đã cli(). */
static void unlock_tick(volatile uint8_t *lock, uint8_t int_bit, uint8_t flag_bit)
{
    if (*lock && --*lock == 0) {
        GIFR = (1 << flag_bit);
        GICR |= (1 << int_bit);
    }
}

int main(void)
{
    LED_DDR = 0xFF;
    ext_int_init();
    sei();

    uint8_t heartbeat = 0;
    for (;;) {
        _delay_ms(TICK_MS);

        cli();
        unlock_tick(&lock0, INT0, INTF0);
        unlock_tick(&lock1, INT1, INTF1);
        uint8_t shown = counter & 0x7F;
        sei();

        if (++heartbeat >= 100)
            heartbeat = 0;                                  /* 100 x 10 ms = 1 s */
        LED_PORT = shown | (heartbeat < 50 ? 0x80 : 0);     /* PC7 = nhịp nền */
    }
}
