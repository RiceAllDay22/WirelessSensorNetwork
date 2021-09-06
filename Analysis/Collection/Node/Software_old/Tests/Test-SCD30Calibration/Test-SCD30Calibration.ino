#include <Wire.h>
#include <SparkFun_SCD30_Arduino_Library.h>
SCD30 airSensor;

uint16_t concData;
uint16_t tempData;
uint16_t humiData;
uint16_t scdData1;
uint16_t scdData2;
uint16_t scdData3;


int CLK = 2;  //CLK->D2
int DT = 3;   //DT->D3
int SW = 4;   //SW->D4

const int interrupt0 = 0;
int count = 750;
int lastCLK = 0; 

void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  Wire.begin();
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT);
  digitalWrite(SW, HIGH);
  attachInterrupt(interrupt0, ClockChanged, CHANGE);


  if (airSensor.begin(Wire, true, true) == false) {
    Serial.println("SCD30 Sensor Failed");
    while (1);
  }

  airSensor.setMeasurementInterval(2);
  airSensor.setAltitudeCompensation(1300);
  airSensor.setTemperatureOffset(0);

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
  if (!digitalRead(SW) && count != 0) {
    uint16_t settingVal;
    airSensor.setForcedRecalibrationFactor(count);
    airSensor.getForcedRecalibration(&settingVal);
    Serial.print("Forced recalibration factor (ppm) is ");
    Serial.println(settingVal);
    delay(1000);
  }

  CollectGas();
  concData = scdData1;
  tempData = scdData2;
  humiData = scdData3;

  Serial.print(millis()/1000); Serial.print(",");
  Serial.print(concData); Serial.print(",");
  Serial.print(tempData); Serial.print(",");
  Serial.println(humiData);
  delay(3000);
}

void ClockChanged() {
  int clkValue = digitalRead(CLK);
  int dtValue = digitalRead(DT);
  if (lastCLK != clkValue){
    lastCLK = clkValue;
    count += (clkValue != dtValue ? 2 : -2);
    Serial.print("count:");
    Serial.println(count);
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
