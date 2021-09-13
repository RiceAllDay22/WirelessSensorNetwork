#include <RTClib.h>
RTC_DS3231 rtc;
DateTime dt;
const byte DETACH_PIN   = 5;

//ADJUST THE UNIXTIME BELOW
uint32_t TIME_VALUE = 1631479650;

void setup() {
  Serial.begin(9600);
  pinMode(DETACH_PIN,   INPUT_PULLUP); 
  RTCBegin();
  //rtc.adjust(TIME_VALUE);
}


void loop() {
  if (digitalRead(DETACH_PIN) == 1) {
    Serial.println("CALIBRATING");
    rtc.adjust(TIME_VALUE);
    delay(5000);
  }
  dt = rtc.now(); 
  Serial.println(dt.unixtime());
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
