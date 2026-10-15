/*
 * Bài 02 - GPIO vào: đọc nút nhấn bằng phương pháp hỏi vòng (polling)
 *
 *   SW1 (PD2): mỗi lần nhấn dịch LED sáng sang trái 1 vị trí (xoay vòng)
 *   SW2 (PD3): mỗi lần nhấn đảo trạng thái toàn bộ LED
 *
 * Chống dội: trạng thái nút phải giữ ổn định DEBOUNCE_MS mới được chấp nhận;
 * chỉ xử lý cạnh xuống (nhả -> nhấn), giữ nút không lặp lại hành động.
 */
#include "board.h"
#include <util/delay.h>
#include <stdint.h>
#include <stdbool.h>

#define DEBOUNCE_MS 20

/* Trả về true đúng một lần cho mỗi lần nhấn đã chống dội. */
static bool button_pressed(uint8_t bit, uint8_t *last_state)
{
    uint8_t now = BTN_PIN & (1 << bit);
    if (now == *last_state)
        return false;

    _delay_ms(DEBOUNCE_MS);
    now = BTN_PIN & (1 << bit);
    if (now == *last_state)
        return false;            /* chỉ là xung nhiễu/dội */

    *last_state = now;
    return now == 0;             /* nhấn = mức 0 */
}

int main(void)
{
    LED_DDR = 0xFF;

    BTN_DDR &= ~((1 << BTN1_BIT) | (1 << BTN2_BIT));
    BTN_PORT |= (1 << BTN1_BIT) | (1 << BTN2_BIT);   /* kéo lên nội, dự phòng R ngoài */

    uint8_t sw1 = 1 << BTN1_BIT;
    uint8_t sw2 = 1 << BTN2_BIT;
    uint8_t pattern = 0x01;
    bool inverted = false;

    for (;;) {
        if (button_pressed(BTN1_BIT, &sw1))
            pattern = (uint8_t)((pattern << 1) | (pattern >> 7));
        if (button_pressed(BTN2_BIT, &sw2))
            inverted = !inverted;

        LED_PORT = inverted ? (uint8_t)~pattern : pattern;
    }
}
