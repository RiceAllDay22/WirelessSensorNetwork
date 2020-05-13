#include "RTClib.h"
RTC_DS3231 rtc;
DateTime dt;

void setup() {
  Serial.begin(9600);
  RTCBegin();
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 1, 14, 9, 0, 0));
}

void loop() {
  dt = rtc.now();
  Serial.println(dt.unixtime());
  delay(1000);
  while (rtc.now().unixtime() == dt.unixtime());
  
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
