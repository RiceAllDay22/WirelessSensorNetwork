#include <Wire.h>
#include <RTClib.h>
RTC_DS3231 rtc;
DateTime dt;
uint32_t TIME_VALUE = 1635233100;

int CLK = 2;  //CLK->D2
int DT = 3;   //DT->D3
int SW = 4;   //SW->D4

const int interrupt0 = 0;
int lastCLK = 0; 


void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  Wire.begin();
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT);
  digitalWrite(SW, HIGH);
  attachInterrupt(interrupt0, ClockChanged, CHANGE);
  RTCBegin();
}

void loop() {
  if (!digitalRead(SW) && TIME_VALUE != 0) {
    rtc.adjust(TIME_VALUE);
    Serial.println("Calibration Complete");
    delay(1000);
  }

  
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

void ClockChanged() {
  int clkValue = digitalRead(CLK);
  int dtValue = digitalRead(DT);
  if (lastCLK != clkValue){
    lastCLK = clkValue;
    TIME_VALUE += (clkValue != dtValue ? 10 : -10);
    Serial.print("TIME_VALUE:");
    Serial.println(TIME_VALUE);
  }
}
