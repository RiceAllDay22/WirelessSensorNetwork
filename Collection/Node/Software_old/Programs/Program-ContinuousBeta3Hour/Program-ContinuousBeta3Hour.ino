//---------------LIBRARIES---------------//
#include <Wire.h>
#include <LowPower.h>
#include <NDIR_I2C.h>
#include <RTClib.h>
#include <SdFat.h>


//---------------VARIABLES---------------//
NDIR_I2C mySensor(0x4D); 
RTC_DS3231 rtc;
SdFat sd;
SdFile file;
DateTime dt;

byte LED_PIN = 2, BUTTON_PIN = 5, DETACH_WIRE = 3; 
const uint8_t sdChipSelect = SS;
float GasData;
uint32_t TimeUnix;
bool wroteNewFile = true;


//---------------SETUP---------------//
void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(DETACH_WIRE, INPUT_PULLUP);

  RTCBegin();
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 4, 5, 20, 5, 0));
  //Serial.println("TimeSet");
  delay(2500);
  MHZ16Begin();
  delay(5000);
  SDBegin();
  delay(2500);
  dt = rtc.now();
  CreateNewFile();
  delay(2500);
}


//---------------MAIN LOOP---------------//
void loop() {
  dt = rtc.now();
  TimeUnix = dt.unixtime();
  GasData  = CollectGas();
  Serial.println(TimeUnix);
  Serial.println(GasData);
  WriteSample();  

  if (dt.minute() == 0 && wroteNewFile == false) {
    wroteNewFile = true;
    file.close();
    CreateNewFile();
  }
  else if (dt.minute() != 0) {
    wroteNewFile = false;
  }
  while (rtc.now().unixtime() == dt.unixtime());
}


//---------------FUNCTIONS---------------//

//----------Create New File----------//
void CreateNewFile() {
  if (digitalRead(DETACH_WIRE)) {
    Serial.println("Not creating new file: (DETATCH_WIRE HIGH)");
    return;
  }
  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour());
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.println("UNIXTIME,CO2");
  file.sync();
  Serial.println("Created new file: " + String(filename));
}

//----------Write Data to SD Card----------//
void WriteSample() {  
  if (digitalRead(DETACH_WIRE)) {
    Serial.println("File Closed: (DETATCH_WIRE HIGH)");
    file.close();
    return;
  }
  digitalWrite(LED_PIN, HIGH);
  String line = String(TimeUnix) + "," + String(GasData);
  file.println(line);
  file.sync();
  //file.close();
  digitalWrite(LED_PIN, LOW);
  Serial.println("Sample Written: " + String(GasData));
}

//----------Retrieve Gas Data----------//
float CollectGas() {
  float data;
  if (mySensor.measure())
    data = mySensor.ppm;
  else
    data = 0.0;
  return data;
}


//---------------STARTUP MODULES---------------//

//----------RTC Begin----------//
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

//----------Gas Begin----------//
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

//----------SD Module Begin ----------//
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
