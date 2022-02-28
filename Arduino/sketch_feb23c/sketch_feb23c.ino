#include <RTClib.h> 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(DateTime(F(__DATE__), F(__TIME__)));
  delay(1000);
}
