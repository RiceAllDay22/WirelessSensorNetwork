const int analogInPin = A0;
int sensorValue = 0;
float outputValue = 0;

void setup() {
  Serial.begin(9600);

}

void loop() {
  sensorValue = analogRead(analogInPin);
  outputValue = sensorValue*5.0/1023;
  Serial.println(outputValue);
  delay(1000);

}
