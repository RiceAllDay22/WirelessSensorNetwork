#include "RTClib.h"
RTC_DS3231 rtc;
DateTime dt;

void setup() {
  Serial.begin(9600);
  pinMode(5, OUTPUT);
  digitalWrite(5, HIGH);
  RTCBegin();
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 1, 14, 9, 0, 0));
}

void loop() {
  digitalWrite(5, HIGH);
  for (int i = 0; i < 10; i++) {
    dt = rtc.now(); 
    Serial.println(dt.unixtime());
    while (rtc.now().unixtime() == dt.unixtime());
  }
  digitalWrite(5, LOW);
  delay(10000);

  
  
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
