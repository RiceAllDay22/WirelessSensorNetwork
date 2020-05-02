//Arduino UNO XBee Receiver Code
#include <SoftwareSerial.h>
SoftwareSerial XBee(2, 3);

void setup() {
  Serial.begin(9600); 
  Serial.println("Receiver");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  XBee.begin(9600);
  Serial.println("Flying is for droids.");
}
 
void loop() {
  if (XBee.available() > 1){
    int data = XBee.read();
    Serial.println(data);
  }
  Serial.println("Nada");
  delay(200);
}
