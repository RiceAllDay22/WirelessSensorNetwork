//Arduino UNO XBee Receiver Code
#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3);
byte LED_PIN    = 5;
int value;

void setup() {
  Serial.begin(9600); 
  Serial.println("Receiver");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  XBee.begin(9600);
  Serial.println("No nothing too fancy.");
}

 
void loop() {
  while (XBee.available()){
    digitalWrite(LED_PIN, HIGH);
    delay(10);
    uint32_t data = XBee.read();
    Serial.println(data);
  }
  digitalWrite(LED_PIN, LOW);
}
