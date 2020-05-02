//Arduino UNO XBee Transmission Code
#include <SoftwareSerial.h>
SoftwareSerial XBee(2, 3);
 
void setup() {
  Serial.begin(9600); 
  Serial.println("Transmitter");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  XBee.begin(9600);
  Serial.println("This is where the fun begins");
}
 
void loop() {
  XBee.write(value);
  delay(100);
}
