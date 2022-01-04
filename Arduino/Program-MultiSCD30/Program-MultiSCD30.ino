#include <Wire.h>
#include <RTClib.h>
#include <SparkFun_SCD30_Arduino_Library.h>

#define TCAADDR 0x70
RTC_DS3231 rtc;
DateTime dt;
DateTime now_dt;
uint32_t now_ut;
SCD30 airSensor0;
SCD30 airSensor1;
SCD30 airSensor2;
SCD30 airSensor3;

int CLK = 2;  //CLK->D2
int DT = 3;   //DT->D3
int SW = 4;   //SW->D4
const int interrupt0 = 0;
int count = 1000;
int lastCLK = 0; 


void setup() {
  //SETUP SERIAL
  Serial.begin(9600);
  Serial.println("");
  Serial.println("SCD30 Example");
  Wire.begin();
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT);
  digitalWrite(SW, HIGH);
  attachInterrupt(interrupt0, ClockChanged, CHANGE);

  //SETUP SENSOR #0
  tcaselect(0);
  if (airSensor0.begin(Wire, false, true) == false) {
    Serial.println("SCD30 Sensor 0 Failed");
    while (1);
  }
  uint16_t settingVal0;
  airSensor0.getAltitudeCompensation(&settingVal0);
  Serial.print("Altitude offset (m) is ");
  Serial.println(settingVal0);
  airSensor0.getMeasurementInterval(&settingVal0);
  Serial.print("Measurement interval (s) is ");
  Serial.println(settingVal0);
  delay(10);

  //SETUP SENSOR #1
  tcaselect(1);
  if (airSensor1.begin(Wire, false, true) == false) {
    Serial.println("SCD30 Sensor 1 Failed");
    while (1);
  }
  uint16_t settingVal1;
  airSensor1.getAltitudeCompensation(&settingVal1);
  Serial.print("Altitude offset (m) is ");
  Serial.println(settingVal1);
  airSensor1.getMeasurementInterval(&settingVal1);
  Serial.print("Measurement interval (s) is ");
  Serial.println(settingVal1);
  delay(10);

  //SETUP SENSOR #2
  tcaselect(2);
  if (airSensor2.begin(Wire, false, true) == false) {
    Serial.println("SCD30 Sensor 2 Failed");
    while (1);
  }
  uint16_t settingVal2;
  airSensor2.getAltitudeCompensation(&settingVal2);
  Serial.print("Altitude offset (m) is ");
  Serial.println(settingVal2);
  airSensor2.getMeasurementInterval(&settingVal2);
  Serial.print("Measurement interval (s) is ");
  Serial.println(settingVal2);
  delay(10);

  //SETUP SENSOR #3
  tcaselect(3);
  if (airSensor3.begin(Wire, false, true) == false) {
    Serial.println("SCD30 Sensor 3 Failed");
    while (1);
  }
  uint16_t settingVal3;
  airSensor3.getAltitudeCompensation(&settingVal3);
  Serial.print("Altitude offset (m) is ");
  Serial.println(settingVal3);
  airSensor3.getMeasurementInterval(&settingVal3);
  Serial.print("Measurement interval (s) is ");
  Serial.println(settingVal3);
  delay(10);
  
  delay(3000);

  //SETUP RTC
  tcaselect(4);
  if(rtc.begin() == false) {
    Serial.println("RTC Failed");
    while (1);
  }
  dt = rtc.now(); 
}

void loop() {
  //CHECK BUTTON PRESS
  if (!digitalRead(SW) && count != 0) {
    tcaselect(0);
    airSensor0.setForcedRecalibrationFactor(count);
    delay(10);
    
    tcaselect(1);
    airSensor1.setForcedRecalibrationFactor(count);
    delay(10);
    
    tcaselect(2);
    airSensor2.setForcedRecalibrationFactor(count);
    delay(10);

    tcaselect(3);
    airSensor3.setForcedRecalibrationFactor(count);
    delay(10);

    Serial.println("Pressed");
    delay(1000);
  }

  
  //GET RTC DATA
  tcaselect(4);
  do {
    now_dt = rtc.now();
    now_ut = now_dt.unixtime();
    delay(50);
  }
  while (now_ut < dt.unixtime() + 3);

  dt = rtc.now(); 
  Serial.print(dt.unixtime());
  Serial.print(", ");


  

  //GET SENSOR #0 DATA
  tcaselect(0);
  Serial.print(airSensor0.getCO2());
  Serial.print(", ");

  //GET SENSOR #1 DATA
  tcaselect(1);
  Serial.print(airSensor1.getCO2());
  Serial.print(", ");

  //GET SENSOR #2 DATA
  tcaselect(2);
  Serial.print(airSensor2.getCO2());
  Serial.print(", ");

  //GET SENSOR #2 DATA
  tcaselect(3);
  Serial.print(airSensor3.getCO2());
  Serial.print(", ");

  //GET CALIBRATION POINT
  Serial.println(count);
  
}


void tcaselect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
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
