#include <RTClib.h>
RTC_DS3231 rtc;
DateTime dt;

void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  RTCBegin();
  //rtc.adjust(1629385450);
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2021, 8, 19, 15, 0, 0));
}

void loop() {
  dt = rtc.now(); 
  Serial.println(dt.unixtime());
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
