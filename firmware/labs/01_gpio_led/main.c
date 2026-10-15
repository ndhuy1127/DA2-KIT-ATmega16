/*
 * Bài 01 - GPIO: điều khiển 8 LED trên PORTC
 *
 * Chạy lần lượt 3 hiệu ứng:
 *   1. Nháy toàn bộ LED (kiểm tra tất cả LED và điện trở hạn dòng)
 *   2. LED chạy từ PC0 -> PC7 (kiểm tra từng chân, phát hiện chân chập/hở)
 *   3. Đếm nhị phân 0..255 (kiểm tra trọng số từng bit)
 *
 * Kiểm thử: quan sát LED trên mô phỏng / bo thật; mỗi bước 200 ms.
 */
#include "board.h"
#include <util/delay.h>
#include <stdint.h>

#define STEP_MS 200

static void blink_all(void)
{
    for (uint8_t i = 0; i < 4; i++) {
        LED_PORT = 0xFF;
        _delay_ms(STEP_MS);
        LED_PORT = 0x00;
        _delay_ms(STEP_MS);
    }
}

static void running_led(void)
{
    for (uint8_t i = 0; i < 8; i++) {
        LED_PORT = (uint8_t)(1u << i);
        _delay_ms(STEP_MS);
    }
}

static void binary_count(void)
{
    uint8_t v = 0;
    do {
        LED_PORT = v;
        _delay_ms(STEP_MS / 4);
    } while (++v != 0);
}

int main(void)
{
    LED_DDR = 0xFF;          /* PORTC: toàn bộ là đầu ra */
    LED_PORT = 0x00;

    for (;;) {
        blink_all();
        for (uint8_t k = 0; k < 2; k++)
            running_led();
        binary_count();
    }
}
