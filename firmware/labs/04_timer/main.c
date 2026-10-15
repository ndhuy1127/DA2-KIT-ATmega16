/*
 * Bài 04 - Timer/Counter
 *
 *   Timer1, chế độ CTC (TOP = OCR1A), đảo chân OC1A (PD5) bằng phần cứng:
 *     f_OC1A = F_CPU / (2 * N * (1 + OCR1A)) = 8 MHz / (2 * 8 * 500) = 1 kHz
 *     -> đo bằng oscilloscope / frequency counter trên mô phỏng để kiểm chứng.
 *   Timer0, chế độ CTC, ngắt mỗi 1 ms:
 *     OCR0 = F_CPU / (64 * 1000) - 1 = 124
 *     -> tạo nhịp hệ thống millis(); PC0 nháy 1 Hz, PC1 nháy 5 Hz,
 *        số giây (mod 64) hiển thị nhị phân trên PC2..PC7.
 */
#include "board.h"
#include <avr/interrupt.h>
#include <stdint.h>

static volatile uint32_t ms_ticks;

ISR(TIMER0_COMP_vect)
{
    ms_ticks++;
}

static uint32_t millis(void)
{
    uint32_t t;
    cli();
    t = ms_ticks;
    sei();
    return t;
}

static void timer0_1ms_init(void)
{
    TCCR0 = (1 << WGM01) | (1 << CS01) | (1 << CS00);   /* CTC, N = 64 */
    OCR0 = (uint8_t)(F_CPU / 64 / 1000 - 1);
    TIMSK |= (1 << OCIE0);
}

static void timer1_1khz_init(void)
{
    OC1A_DDR |= (1 << OC1A_BIT);
    TCCR1A = (1 << COM1A0);                     /* đảo OC1A mỗi lần so khớp */
    TCCR1B = (1 << WGM12) | (1 << CS11);        /* CTC (TOP = OCR1A), N = 8 */
    OCR1A = (uint16_t)(F_CPU / (2UL * 8 * 1000) - 1);
}

int main(void)
{
    LED_DDR = 0xFF;
    LED_PORT = 0;

    timer0_1ms_init();
    timer1_1khz_init();
    sei();

    uint32_t t_slow = 0, t_fast = 0;
    uint8_t seconds = 0, leds = 0;

    for (;;) {
        uint32_t now = millis();

        if (now - t_fast >= 100) {              /* 5 Hz: đảo mỗi 100 ms */
            t_fast += 100;
            leds ^= 0x02;
        }
        if (now - t_slow >= 500) {              /* 1 Hz: đảo mỗi 500 ms */
            t_slow += 500;
            leds ^= 0x01;
            if (!(leds & 0x01))
                seconds = (seconds + 1) & 0x3F;
        }
        LED_PORT = (uint8_t)((seconds << 2) | (leds & 0x03));
    }
}
