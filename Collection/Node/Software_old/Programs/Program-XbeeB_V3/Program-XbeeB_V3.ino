//Arduino UNO XBee Receiver Code
#include <SoftwareSerial.h>

SoftwareSerial XBee(2, 3);
byte WIRE_PIN   = 11;
byte BUTTON_PIN = 12;
byte LED_PIN    = 5;
int value = 49;


void setup() {
  Serial.begin(9600); 
  Serial.println("Receiver");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(WIRE_PIN, INPUT_PULLUP);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  XBee.begin(9600);
  Serial.println("Flying is for droids.");
}

 
void loop() {
  if (digitalRead(WIRE_PIN)) value = 49;
  else value = 50;
  
  if (digitalRead(BUTTON_PIN) == LOW) {
    XBee.write(value);
    Serial.println(value);
    delay(200);
  }
  
  while (XBee.available()){
    digitalWrite(LED_PIN, HIGH);
    char data = XBee.read();
    Serial.print(data);
  }
  digitalWrite(LED_PIN, LOW);
}
