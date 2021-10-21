#include "sw_uart.h"

due_sw_uart uart_TX;

void setup_TX() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 4, 1, 8, SW_UART_EVEN_PARITY);
}

void loop_TX() {
 test_write();
}

void test_write() {
  sw_uart_write_string(&uart, "a");
  delay(1000);
}
