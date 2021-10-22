#include "sw_uart.h"

due_sw_uart uart;
char teste = 'a';
//a em binario = 01100001

void setup() {
  //Serial.begin(9600);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  delay(1000);
}

void loop() {
  digitalWrite(4, LOW);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, HIGH);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, LOW);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, LOW);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, LOW);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, LOW);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, HIGH);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, HIGH);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, LOW);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, HIGH);
  sw_uart_delay_H();
  sw_uart_delay_H();
  digitalWrite(4, HIGH);
  delay(1000);
 //test_write();
}

void sw_uart_delay_H() {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}
