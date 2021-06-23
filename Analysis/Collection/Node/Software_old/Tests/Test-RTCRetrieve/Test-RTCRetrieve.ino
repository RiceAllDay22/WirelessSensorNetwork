#include <RTClib.h>
RTC_DS3231 rtc;
DateTime dt;

void setup() {
  Serial.begin(9600);
  RTCBegin();
  
  //Uncomment the code below to set the clock to a specific timestamp to synchronize.
  //Comment out the code below then synchronization is complete.
  //rtc.adjust(1624384200);
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
