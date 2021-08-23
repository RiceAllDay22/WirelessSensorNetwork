//---------------LIBRARIES---------------//
//---------------------------------------//
#include <Wire.h>
#include <RTClib.h>
#include <SdFat.h>
#include <SparkFun_SCD30_Arduino_Library.h> 


//---------------VARIABLES---------------//
//---------------------------------------//
SdFat       sd;
SdFile      file;
RTC_DS3231  rtc;
DateTime    now_dt;
DateTime    dt;
DateTime    filestart_dt;
SCD30       airSensor;

uint32_t ut;
uint32_t now_ut;
uint32_t filestart_ut;

const byte sdChipSelect = SS;
const byte WSPEED_PIN   = 2;
const byte DETACH_PIN   = 5;
const byte LED_PIN      = 6;

const int arrayLength = 5;
uint32_t  unixTime[arrayLength];
uint8_t   windCyc[arrayLength];
uint16_t  windDir[arrayLength];
uint16_t  concData[arrayLength];
uint8_t   tempData[arrayLength];
uint16_t  scdData1;
uint8_t   scdData2;

bool wroteNewFile = true;
volatile byte windClicks  = 0;
volatile unsigned long lastWindIRQ = 0;

uint16_t VaneValue;
uint16_t Direction;
uint16_t CalDirection;
#define  Offset 45;  

void(* resetFunc)(void) = 0;                //declare reset function at address 0

//---------------SETUP-------------------//
//---------------------------------------//
void setup() {
  Serial.begin(9600);
  Serial.println("Setup Begin");
  
  Wire.begin();
  pinMode(LED_PIN,      OUTPUT);
  pinMode(WSPEED_PIN,   INPUT);
  pinMode(DETACH_PIN,   INPUT_PULLUP); 
  digitalWrite(LED_PIN, HIGH);

  RTCBegin();
  
  SCD30Begin();
  airSensor.setMeasurementInterval(2);                  // # seconds between readings
  airSensor.setAltitudeCompensation(1300);              // # meter above sea level
  //airSensor.setForcedRecalibrationFactor(420);
  uint16_t settingVal;
  airSensor.getForcedRecalibration(&settingVal);
  Serial.print("Forced recalibration factor (ppm) is ");
  Serial.println(settingVal);
  
  SDBegin();
  dt = rtc.now();
  filestart_dt = dt;
  filestart_ut = filestart_dt.unixtime();
  CreateNewFile();
  delay(2000);
  
  attachInterrupt(digitalPinToInterrupt(WSPEED_PIN), isr_rotation, FALLING);
  interrupts();
 
  digitalWrite(LED_PIN, LOW);
  Serial.println("Setup Complete");
}


//--------------MAIN LOOP----------------//
//---------------------------------------//
void loop() {
  now_dt = rtc.now();
  
  for (int i=0; i<arrayLength; i++) {
    dt           = now_dt;
    ut           = dt.unixtime();
    unixTime[i]  = ut;
    windDir[i]   = WindDirection(); 
    CollectGas();
    concData[i]  = scdData1;
    tempData[i]  = scdData2;


    Serial.println();
    Serial.print(ut);
    Serial.print(" ");

    do {



      Serial.print("Stuck1?");
      now_dt = rtc.now();
      now_ut = now_dt.unixtime();
      Serial.print(now_ut);
      Serial.print(" ");
      delay(100);


      
      Serial.print("Stuck2?");
      if (now_ut > ut + 604800) {
        Serial.println("Time Jump Occurred");
        delay(100);


        Serial.print("Stuck3?");
        now_dt = rtc.now();
        now_ut = now_dt.unixtime();;
      }


      Serial.print("Stuck4?");
    } while ( now_ut < ut + 3 );

    Serial.print("Stuck4.5?");
    windCyc[i] = windClicks;
    windClicks = 0;
    Serial.print("Stuck4.7?");
    
  }

  Serial.print("Stuck5?");
  WriteSample();

  Serial.print("Stuck6?");
  if (filestart_ut + 1800 <= ut) {
    filestart_dt = dt;
    filestart_ut = filestart_dt.unixtime();
    file.close();
    delay(5000);
    CreateNewFile();
    //resetFunc();
  }
}   

//-------------FILE HANDLING-------------//
//---------------------------------------//
void CreateNewFile() {
  if (digitalRead(DETACH_PIN)) {
    Serial.println("DETATCH_PIN HIGH");
    return;
  }
  //char filename[19];
  //sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour());
  char filename[22];
  sprintf(filename, "%04d-%02d-%02d--%02d-%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour(), dt.minute());
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  delay(1000);
  file.sync();
  Serial.println("Created new file.");
}

void WriteSample() {  
  if (digitalRead(DETACH_PIN)) {
    Serial.println("File Closed: (DETATCH_PIN HIGH)");
    digitalWrite(LED_PIN, HIGH);
    file.close();
    return;
  }

  else {
    digitalWrite(LED_PIN, HIGH);
  
    for (int j=0; j<arrayLength; j++) {
      file.write((unixTime[j] >> 24) & 0xFF);
      file.write((unixTime[j] >> 16) & 0xFF);
      file.write((unixTime[j] >> 8)  & 0xFF);
      file.write((unixTime[j] >> 0)  & 0xFF);
      file.write((windCyc[j]  >> 0)  & 0xFF);
      file.write((windDir[j]  >> 8)  & 0xFF);
      file.write((windDir[j]  >> 0)  & 0xFF);
      file.write((concData[j] >> 8)  & 0xFF);
      file.write((concData[j] >> 0)  & 0xFF);
      file.write((tempData[j] >> 0)  & 0xFF);
    }
    
    file.sync();
    digitalWrite(LED_PIN, LOW);
  }
}


//--------DATA RETRIEVAL FUNCTIONS-------//
//---------------------------------------//

//------Retrieve Conc and Temp Data------//
void CollectGas() {
  if (airSensor.dataAvailable()) {
    scdData1 = airSensor.getCO2();
    scdData2 = airSensor.getTemperature();
  }
  else {
    delay(5);
    if (airSensor.dataAvailable()) {
      scdData1 = airSensor.getCO2();
      scdData2 = airSensor.getTemperature();
    }
    else {
      scdData1 = 0;
      scdData2 = 0;
    }  
  }
}

//----------Retrieve Wind Speed----------//
void isr_rotation() {
  if ((unsigned long)( millis() - lastWindIRQ) > 15 ) {
    lastWindIRQ = millis(); 
    windClicks++;           
  }
}


//--------Retrieve Wind Direction-------//
uint16_t WindDirection() {
  VaneValue    = analogRead(A3);
  Direction    = map(VaneValue, 0, 1023, 1, 360);
  CalDirection = Direction + Offset;

  if (CalDirection > 360)
    CalDirection = CalDirection - 360;
  if (CalDirection < 1)
    CalDirection = CalDirection + 360;
  return (CalDirection);
}


//----------STARTUP MODULES---------------//
//---------------------------------------//

//----------RTC Begin----------//
void RTCBegin() {
  bool success = false;
  while (success == false) {
    if(rtc.begin()) {
      success = true;
    }
    else {
      Serial.println("RTC Failed");
    }
    delay(2000);
  }
  Serial.println("RTC Operational");
}


//----------Gas Begin----------//
void SCD30Begin() {
  bool success = false;
  while (success == false) {
    if(airSensor.begin(Wire, true, true)) {
      success = true;
      }      
    else {
      Serial.println("Sensor Failed");
    }
    delay(2000); 
  }
  Serial.println("Sensor Operational");
}


//----------SD Module Begin ----------//
void SDBegin() {
  bool success = false;
  while (success == false) {
    if(sd.begin(sdChipSelect)) {
      success = true; 
    }
    else {
      Serial.println("SD Module Failed");
    }
    delay(2000);
  }
  Serial.println("SD Module Operational");
}
