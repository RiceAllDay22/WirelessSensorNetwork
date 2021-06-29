#include <Wire.h>
#include <SparkFun_SCD30_Arduino_Library.h>
SCD30 airSensor;

uint16_t gasData;
uint16_t tempData;
uint16_t scdData1;
uint16_t scdData2;

void setup() {
  Serial.begin(9600);
  Serial.println("SCD30 Example");
  Wire.begin();

  if (airSensor.begin() == false) {
    Serial.println("Air sensor not detected.");
    while (1) ;
  }
}

void loop() {
  CollectGas();
  gasData  = scdData1;
  tempData = scdData2;

  Serial.print(millis());  Serial.print(",");
  Serial.print(gasData); Serial.print(",");
  Serial.println(tempData);
  delay(3000);
}


void CollectGas() {
  if (airSensor.dataAvailable()) {
    scdData1 = airSensor.getCO2();
    scdData2 = airSensor.getTemperature();
  }
  else {
    delay(5);
    if (airSensor.dataAvailable()) {
      scdData1 = airSensor.getCO2();
      scdData2 = airSensor.getTemperature();
    }
    else {
      scdData1 = 0;
      scdData2 = 0;
    }  
  }
}
