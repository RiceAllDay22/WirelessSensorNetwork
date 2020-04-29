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
float gasData;
const uint8_t sdChipSelect = SS;
bool wroteNewFile = true;

RTC_DS3231 rtc;

void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(DETACH_WIRE, INPUT_PULLUP);
  
  RTCBegin();
  MHZ16Begin();
  SDBegin();

  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 3, 1, 19, 0, 1));

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
  String line = String(dt.unixtime()) + "," + String(gasData);
  file.println(line);
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
  file.println("UNIXTIME,CO2");  // write CSV headers
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
  float data;
  if (mySensor.measure())
    data = mySensor.ppm;
  else
    data = -1;
  return data;
}
