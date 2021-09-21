#include <Wire.h>
#define TCAADDR 0x70
#include <SparkFun_SCD30_Arduino_Library.h>

SCD30 airSensor0;
SCD30 airSensor1;

void setup() {
  Serial.begin(9600);
  Serial.println("");
  Serial.println("SCD30 Example");
  Wire.begin();

  tcaselect(0);
  if (airSensor1.begin(Wire, true, true) == false) {
    Serial.println("SCD30 Sensor 0 Failed");
    while (1);
  }

  tcaselect(1);
  if (airSensor.begin(Wire, true, true) == false) {
    Serial.println("SCD30 Sensor 1 Failed");
    while (1);
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}


void tcaselect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}
