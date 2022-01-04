#include <RTClib.h>
RTC_DS3231 rtc;
DateTime dt;
int counter = 0;
void(* resetFunc)(void) = 0;//declare reset function at address 0


void setup() {
  Serial.begin(9600);
  Serial.println("Starting");
  RTCBegin();
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 1, 14, 9, 0, 0));
}

void loop() {
  counter ++;
  dt = rtc.now(); 
  Serial.println(dt.unixtime());
  while (rtc.now().unixtime() == dt.unixtime());

  if (counter == 10) {
    resetFunc();
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
