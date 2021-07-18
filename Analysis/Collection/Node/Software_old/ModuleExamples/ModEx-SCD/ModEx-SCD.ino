//Click here to get the library: http://librarymanager/All#SparkFun_SCD30

#include <Wire.h>
#include <SparkFun_SCD30_Arduino_Library.h>
SCD30 airSensor;

uint16_t concData;
uint16_t tempData;
uint16_t humiData;
uint16_t scdData1;
uint16_t scdData2;
uint16_t scdData3;

void setup() {
  Serial.begin(9600);
  Serial.println("");
  Serial.println("SCD30 Example");
  Wire.begin();

  //bool begin(TwoWire &wirePort = Wire, bool autoCalibrate = false, bool measBegin = true);
  if (airSensor.begin(Wire, false, true) == false) {
    Serial.println("SCD30 Sensor Failed");
    while (1);
  }

  airSensor.setMeasurementInterval(2);
  airSensor.setAltitudeCompensation(1300);
  airSensor.setTemperatureOffset(0);
  //airSensor.setForcedRecalibrationFactor()
  //airSensor.setAutoSelfCalibration()
  
  

  uint16_t settingVal;

  airSensor.getFirmwareVersion(&settingVal);
  Serial.print("Firmware version is 0x");
  Serial.println(settingVal, HEX);
    
  airSensor.getMeasurementInterval(&settingVal);
  Serial.print("Measurement interval (s) is ");
  Serial.println(settingVal);
  
  airSensor.getTemperatureOffset(&settingVal);
  Serial.print("Temperature offfset (C) is ");
  Serial.println(((float)settingVal) / 100.0, 2);
  
  airSensor.getAltitudeCompensation(&settingVal);
  Serial.print("Altitude offset (m) is ");
  Serial.println(settingVal);
  
  airSensor.getForcedRecalibration(&settingVal);
  Serial.print("Forced recalibration factor (ppm) is ");
  Serial.println(settingVal);

  Serial.print("Auto calibration set to ");
  Serial.println(airSensor.getAutoSelfCalibration());
  
}

void loop() {
  CollectGas();
  concData = scdData1;
  tempData = scdData2;
  humiData = scdData3;

  Serial.print(millis()/1000); Serial.print(",");
  Serial.print(concData); Serial.print(",");
  Serial.print(tempData); Serial.print(",");
  Serial.println(humiData);
  delay(3000);

  if ( (millis() > 120000) && (millis() < 123000) ) {
    uint16_t settingVal;
    airSensor.setForcedRecalibrationFactor(1000);
    airSensor.getForcedRecalibration(&settingVal);
    Serial.print("Forced recalibration factor (ppm) is ");
    Serial.println(settingVal);
  } 
}

void CollectGas() {
  if (airSensor.dataAvailable()) {
    scdData1 = airSensor.getCO2();
    scdData2 = airSensor.getTemperature();
    scdData3 = airSensor.getHumidity();
  }
  else {
    delay(5);
    if (airSensor.dataAvailable()) {
      scdData1 = airSensor.getCO2();
      scdData2 = airSensor.getTemperature();
      scdData3 = airSensor.getHumidity();
    }
    else {
      scdData1 = 0;
      scdData2 = 0;
      scdData3 = 0;
    }  
  }
}

void NewCollectGas() {
  scdData1 = airSensor.getCO2();
  scdData2 = airSensor.getTemperature();
  scdData3 = airSensor.getHumidity();
}
