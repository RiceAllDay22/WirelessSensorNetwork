/*
Adriann Liceralde and Jacob Larkin
Energy & Geoscience Institute at the University of Utah

Origin code from SparkFun Electronics
License: MIT.
*/

#include <Wire.h>
#include "SparkFun_SCD30_Arduino_Library.h"  //Click here to get the library: http://librarymanager/All#SparkFun_SCD30

SCD30 airSensor;

void setup() {
  //-----BEGIN SENSOR-----//
  Serial.begin(9600);
  Serial.println("SCD30 Example");
  Wire.begin();

  if (airSensor.begin(Wire, false) == false) {
    Serial.println("Air sensor not detected. Please check wiring. Freezing...");
      while (1);
  }


  //-----SPECIFY SETTINGS-----//
  airSensor.setMeasurementInterval(2);      //Change number of seconds between measurements: 2 to 1800 (30 minutes)
  airSensor.setAltitudeCompensation(30);    //Set altitude of the sensor in m, stored in non-volatile memory of SCD30
  //airSensor.setAmbientPressure(835);      //Current ambient pressure in mBar: 700 to 1200, will overwrite altitude compensation
  //airSensor.setTemperatureOffset(5);      //Optionally we can set temperature offset to 5°C, stored in non-volatile memory of SCD30


  //-----CHECK SETTINGS-----//
  Serial.print("Auto calibration set to ");
  Serial.println(airSensor.getAutoSelfCalibration());

  uint16_t settingVal; // The settings will be returned in settingVal
  
  airSensor.getForcedRecalibration(&settingVal);
  Serial.print("Forced recalibration factor (ppm) is ");
  Serial.println(settingVal);
  
  airSensor.getMeasurementInterval(&settingVal);
  Serial.print("Measurement interval (s) is ");
  Serial.println(settingVal);
  
  airSensor.getTemperatureOffset(&settingVal);
  Serial.print("Temperature offfset (C) is ");
  Serial.println(((float)settingVal) / 100.0, 2);
  
  airSensor.getAltitudeCompensation(&settingVal);
  Serial.print("Altitude offset (m) is ");
  Serial.println(settingVal);
  
  airSensor.getFirmwareVersion(&settingVal);
  Serial.print("Firmware version is 0x");
  Serial.println(settingVal, HEX);
  
}

void loop() {
  if (airSensor.dataAvailable()) {
    Serial.print("co2(ppm):");
    Serial.print(airSensor.getCO2());
    Serial.print(" temp(C):");
    Serial.print(airSensor.getTemperature(), 1);
    Serial.print(" humidity(%):");
    Serial.println(airSensor.getHumidity(), 1);
  }
  else
    Serial.println("Waiting for new data");
  delay(2000);
}
