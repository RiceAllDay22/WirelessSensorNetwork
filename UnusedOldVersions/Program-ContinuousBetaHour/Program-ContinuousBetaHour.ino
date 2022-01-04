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
const uint8_t sdChipSelect = SS;
String string2, string4, string6, temp;
String string1 = "Month", string3 = "Day", string5 = "Hour", string7 = ".csv";

float GasData;
uint32_t TimeUnix;
byte LED_PIN = 2, BUTTON_PIN = 5, DETACH_WIRE = 3; 
int  TimeMonth, TimeDay, TimeHour, TimeMinute, TimeSecond;
bool HourCheck1, HourCheck2, HourCheck3, newHour;


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
  MHZ16Begin();
  SDBegin();

  dt = rtc.now();
  TimeMonth = dt.month();
  TimeDay   = dt.day();
  TimeHour  = dt.hour();
  newFile();
  delay(3000);
}


//---------------MAIN LOOP---------------//
void loop() {
  GasData  = CollectGas();
  dt = rtc.now();
  
  TimeUnix   = dt.unixtime();
  TimeMonth  = dt.month();
  TimeDay    = dt.day();
  TimeHour   = dt.hour();
  TimeMinute = dt.minute();
  TimeSecond = dt.second();
  
  Serial.print(TimeMonth);  Serial.print(','); Serial.print(TimeDay);    Serial.print(',');
  Serial.print(TimeHour);   Serial.print(','); Serial.print(TimeMinute); Serial.print(','); 
  Serial.print(TimeSecond); Serial.print(','); Serial.print(TimeUnix);   Serial.print(',');
  Serial.println(GasData);

  if (newHour == false) { 
    if (TimeMinute == 0 and TimeSecond == 0) HourCheck1 = true;
    if (TimeMinute == 0 and TimeSecond == 1) HourCheck2 = true;
    if (TimeMinute == 0 and TimeSecond == 2) HourCheck3 = true;
    if(HourCheck1 == true or HourCheck2 == true or HourCheck3 == true) newHour = true;
    Serial.println(newHour);
  }
  if (newHour == true) {
    if (TimeSecond > 2) {
      newHour = false; HourCheck1 = false; HourCheck2 = false; HourCheck3 = false;
      Serial.println("New File");
      newFile();  
    }
  }
  WriteData();  
  while (rtc.now().unixtime() == dt.unixtime());
}


//---------------FUNCTIONS---------------//

//----------Create New File----------//
void newFile() {
  file.sync();
  file.close();
  string2 = String(TimeMonth);
  string4 = String(TimeDay);
  string6 = String(TimeHour);
  temp = String(string1 + string2 + string3 + string4 + string5 + string6 + string7);
  char filename[temp.length()+1];
  temp.toCharArray(filename, sizeof(filename));
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.print("UNIXTIME"); file.print(','); file.println("CO2"); 
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


//----------Write Data to SD Card----------//
void WriteData() {
  if (!digitalRead(DETACH_WIRE)) {
    digitalWrite(LED_PIN, HIGH);
    file.print(TimeUnix);file.print(',');file.println(GasData);
    digitalWrite(LED_PIN, LOW);
  }
  else {
    Serial.println("File Closed");
    file.sync();
    file.close();
  }
}


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
