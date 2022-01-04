#include <RTClib.h>
//#include <Wire.h>
RTC_DS3231 rtc;
DateTime dt;

void setup() {
  Serial.begin(9600);
  //Wire.setClock(32000);
  RTCBegin();
  //rtc.adjust(1631319900);

}

void loop() {
  //Wire.beginTransmission(0x68);
  //Wire.write(0x0F);
  //Wire.endTransmission();

  //Wire.requestFrom(0x68, 1);
  //byte y = Wire.read();
  //Serial.print(y); Serial.print(",");

  //if ( (y & 0x80) != 0x80) {
  //  Serial.print("Running");
  //}
  //else {
  //  Serial.print("No");
  //}
  //Serial.print(",");

  Serial.print(rtc.lostPower()); Serial.print(",");
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
