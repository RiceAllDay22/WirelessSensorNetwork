#include <Wire.h>
#include <NDIR_I2C.h>
#include <RTClib.h>//
#include <SdFat.h>

byte DETACH_WIRE = 3;
byte LED_PIN     = 2;
NDIR_I2C mySensor(0x4D); 


SdFat sd;
SdFile file;
DateTime dt;
int gasData;
const uint8_t sdChipSelect = SS;
bool wroteNewFile = true;

RTC_DS3231 rtc;

void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(DETACH_WIRE, INPUT_PULLUP);
  
  RTCBegin();
  //rtc.adjust(DateTime(2020, 3, 5, 18, 54, 1));
  MHZ16Begin();
  SDBegin();
  
  dt = rtc.now();
  
  CreateNewFile();
}

void loop() {
  // loop until next sample
  while (rtc.now().unixtime() < dt.unixtime() + 1);
  
  gasData = CollectGas(); 
  //
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

  file.write((dt.unixtime() >> 24) & 0xFF);
  file.write((dt.unixtime() >> 16) & 0xFF);
  file.write((dt.unixtime() >> 8) & 0xFF);
  file.write((dt.unixtime() >> 0) & 0xFF);

  file.write((gasData >> 24) & 0xFF);
  file.write((gasData >> 16) & 0xFF);
  file.write((gasData >> 8) & 0xFF);
  file.write((gasData >> 0) & 0xFF);
  
  file.sync();
  digitalWrite(LED_PIN, LOW);
  Serial.println("Sample Written: " + String(gasData));
}

void CreateNewFile() {
  if (digitalRead(DETACH_WIRE)) {
    Serial.println("Not creating new file: (DETATCH_WIRE HIGH)");
    return;
  }

  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(),
          dt.hour());
  
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  //file.println("UNIXTIME,CO2");  // write CSV headers
  file.sync();
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

void MHZ16Begin() {
  bool success = false;
  while (success == false) {
    if(mySensor.begin())
      success = true;
    else
      Serial.println("Sensor Failed");
    delay(1000);
  }
  Serial.println("Sensor Operational");
}

float CollectGas() {
  int data;
  if (mySensor.measure())
    data = mySensor.ppm;
  else
    data = -1;
  return data;
}
