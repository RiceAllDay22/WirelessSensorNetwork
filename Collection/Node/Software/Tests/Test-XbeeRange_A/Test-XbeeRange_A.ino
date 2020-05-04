//Arduino UNO XBee Continuous Transmission Code
#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3);
int value = 49;

void setup() {
  Serial.begin(9600); 
  Serial.println("Transmission");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  XBee.begin(9600);
  Serial.println("Flying is for droids.");
}

 
void loop() {
  XBee.write(value);
  Serial.println(value);
  delay(500);
  }
