#include <Wire.h>
#include <SparkFun_SCD30_Arduino_Library.h> 

SCD30 airSensor;
unsigned long nowTime;
unsigned long lastTime;
unsigned long deltaTime;

void setup() {
  Serial.begin(9600);
  Serial.println("SCD30 Example");
  Wire.begin();

  if (airSensor.begin() == false) {
    Serial.println("Air sensor not detected");
    while (1);
  }

  airSensor.setMeasurementInterval(2);
  lastTime = 0;
  nowTime  = millis();
}

void loop() {
  nowTime = millis();
  if (airSensor.dataAvailable()) {
    deltaTime = nowTime - lastTime;
    lastTime  = nowTime;
    
    Serial.print(deltaTime);
    Serial.print(" ");
    Serial.print(airSensor.getCO2());
    Serial.println();
  }
}
