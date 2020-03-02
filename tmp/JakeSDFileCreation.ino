/*
File writes fake gas data and unixtime to sd card with option of a fast fake clock.

This file is a part of Wireless Sensor Project
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/


#include <Wire.h>
#include <RTClib.h>//
#include <SdFat.h>

byte DETACH_WIRE = 3;
byte LED_PIN     = 2;


SdFat sd;
SdFile file;
DateTime dt;
float gasData;
const uint8_t sdChipSelect = SS;
bool wroteNewFile = true;

class FastClock {  // for testing clock hours
  DateTime current;
  long start_unixtime = DateTime(2020, 3, 1, 10, 0, 0).unixtime();
  int count = 0;
  int count2 = 0;

  public:
  FastClock() {
    current = DateTime(start_unixtime);
  }

  bool begin() {
      return true;
  }
  
  DateTime now() {
    current = DateTime(start_unixtime + count);
    
    count2++;
    if (count2 == 3) {
      count2 = 0;
      count++;
    }
    
    return current;
  }
};

//RTC_DS3231 rtc;
FastClock rtc;

void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(DETACH_WIRE, INPUT_PULLUP);
  
  RTCBegin();
  SDBegin();

  dt = rtc.now();
  
  file = CreateNewFile();
}

void loop() {
  // loop until next sample
  while (rtc.now().unixtime() < dt.unixtime() + 1);
  
  float gasData = 1;
  dt = rtc.now();

  WriteSample();
 
  if (dt.minute() == 0 && wroteNewFile == false) {
    wroteNewFile = true;
    file.close();
    CreateNewFile();
  }
  else if (dt.minute() != 0) {
    wroteNewFile = false;
  }
}

void WriteSample() {  
  if (digitalRead(DETACH_WIRE)) {
    Serial.println("File Closed: (DETATCH_WIRE HIGH)");
    file.close();
    return;
  }
  
  digitalWrite(LED_PIN, HIGH);
  String line = String(dt.unixtime()) + "," + String(gasData);
  file.println(line);
  file.sync();
  digitalWrite(LED_PIN, LOW);
  // Serial.println("Sample Written");
}

SdFile CreateNewFile() {
  if (digitalRead(DETACH_WIRE)) {
    Serial.println("Not creating new file: (DETATCH_WIRE HIGH)");
    return;
  }

  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(),
          dt.hour());
  
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.println("UNIXTIME,CO2");  // write CSV headers
  Serial.println("Created new file: " + String(filename));
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


void SDBegin() {
  bool success = false;
  while (success == false) {
    if(sd.begin(sdChipSelect))
      success = true;
    else
      Serial.println("SD Module Failed");
    delay(1000);
  }
  Serial.println("SD Module Operational");
}
