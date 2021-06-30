#include <Wire.h>
#include <SparkFun_SCD30_Arduino_Library.h> 
#include <RTClib.h>

RTC_DS3231 rtc;
DateTime dtnow;
DateTime dtlast;

SCD30 airSensor;
unsigned long nowTime;
unsigned long lastTime;
unsigned long deltaTime;
unsigned long dtdelta;

void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  Wire.begin();
  RTCBegin();

  if (airSensor.begin() == false) {
    Serial.println("Air sensor not detected");
    while (1);
  }

  airSensor.setMeasurementInterval(2); // in seconds
  lastTime = 0;
  nowTime  = millis();
}

void loop() {
  nowTime = millis();
  dtnow   = rtc.now(); 
  if (airSensor.dataAvailable()) {
    deltaTime = nowTime - lastTime;
    lastTime  = nowTime;

    dtdelta = dtnow.unixtime()-dtlast.unixtime();
    dtlast  = dtnow;
    Serial.print(dtdelta);    Serial.print(" ");
    Serial.print(deltaTime);  Serial.print(" ");
    Serial.println(airSensor.getCO2());
  }
}


void RTCBegin() {
  bool success = false;
  while (success == false) {
    if(rtc.begin())
      success = true;
    else
      Serial.println("RTC Failed");
    delay(1000);
  }
  Serial.println("RTC Operational");
}
