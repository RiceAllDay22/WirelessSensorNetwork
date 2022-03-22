#include <Wire.h>
#include <RTClib.h>

extern "C" {
  #include "utility/twi.h"
}

#define TCAADDR 0x70

RTC_DS3231 rtc0;
RTC_DS3231 rtc1;
RTC_DS3231 rtc2;
RTC_DS3231 rtc3;
DateTime dt0;
DateTime dt1;
DateTime dt2;
DateTime dt3;

const byte DETACH_PIN   = 5;


void tcaselect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pinMode(DETACH_PIN,   INPUT_PULLUP);
  

  //SETUP RTC #0
  tcaselect(0);
    if(rtc0.begin() == false) {
    Serial.println("RTC 0 Failed");
    while (1);
  }
  dt0 = rtc0.now(); 

  //SETUP RTC #1
  tcaselect(1);
    if(rtc1.begin() == false) {
    Serial.println("RTC 1 Failed");
    while (1);
  }
  dt1 = rtc1.now(); 

  
  //SETUP RTC #2
  tcaselect(2);
    if(rtc2.begin() == false) {
    Serial.println("RTC 2 Failed");
    while (1);
  }
  dt2 = rtc2.now(); 


  //SETUP RTC #3
  tcaselect(3);
    if(rtc3.begin() == false) {
    Serial.println("RTC 3 Failed");
    while (1);
  }
  dt3 = rtc3.now();   
  
}

void loop() {
  tcaselect(0);
  dt0 = rtc0.now(); 
  Serial.print(dt0.minute());
  Serial.print(",");
  Serial.print(dt0.second());
  Serial.print(",");

  tcaselect(1);
  dt1 = rtc1.now(); 
  Serial.print(dt1.minute());
  Serial.print(",");
  Serial.print(dt1.second());
  Serial.print(",");
  
  tcaselect(2);
  dt2 = rtc2.now(); 
  Serial.print(dt2.minute());
  Serial.print(",");
  Serial.print(dt2.second());
  Serial.print(",");
  
  tcaselect(3);
  dt3 = rtc3.now(); 
  Serial.print(dt3.minute());
  Serial.print(",");
  Serial.println(dt3.second());

  delay(1000);


  if (digitalRead(DETACH_PIN) == 1) {
    Serial.println("CALIBRATING");
    tcaselect(0);
    //rtc0.adjust(DateTime(2022, 3, 22, 5, 41, 0));
    tcaselect(1);
    //rtc1.adjust(DateTime(2022, 3, 22, 5, 41, 0));
    tcaselect(2);
    //rtc2.adjust(DateTime(2022, 3, 22, 5, 41, 0));
    tcaselect(3);
    //rtc3.adjust(DateTime(2022, 3, 22, 5, 41, 0));
    delay(5000);
  }
}
