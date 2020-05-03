//Arduino UNO XBee Receiver Code
#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3);
byte BUTTON_PIN = 5;

void setup() {
  Serial.begin(9600); 
  Serial.println("Receiver");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  XBee.begin(9600);
  Serial.println("Flying is for droids.");
}

 
void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    XBee.write(50);
    Serial.println(2);
    delay(200);
  }
  
  while (XBee.available()){
    char data = XBee.read();
    Serial.print(data);
  }
}
