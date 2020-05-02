//Arduino UNO XBee Transmission Code
#include <SoftwareSerial.h>
SoftwareSerial XBee(2, 3);
byte BUTTON_PIN = 12;
 
void setup() {
  Serial.begin(9600); 
  Serial.println("Transmitter");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  XBee.begin(9600);
  Serial.println("Ah yes the negotiator");
}
 
void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("Fine collection");
    for (uint8_t value = 10; value < 250; value = value+10) {
      XBee.write(value);
    }
    delay(100);
  }
}
