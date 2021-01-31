int value = 200;
int PIN = 7;
#include <SoftwareSerial.h>
SoftwareSerial XBee(2, 3);

void setup() {
  XBee.begin(9600);
  Serial.begin(9600);
  Serial.println("Xbee - B Enabled");
  pinMode(PIN, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(PIN) == LOW) {
    Serial.println(value);
    XBee.write(value);
    delay(200); 
  }
  
  while (XBee.available()) {
    Serial.write(XBee.read());
  }
  //Serial.println("Hello there");
  delay(5);
}
