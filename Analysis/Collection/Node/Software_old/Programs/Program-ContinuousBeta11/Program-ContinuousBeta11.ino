//---------------LIBRARIES---------------//
//---------------------------------------//
#include <Wire.h>
#include <RTClib.h>
#include <SdFat.h>
#include <SparkFun_SCD30_Arduino_Library.h> 
//#include <LowPower.h>
//#include <LiquidCrystal_I2C.h>
//#include <SPI.h>


//---------------VARIABLES---------------//
//---------------------------------------//
SdFat sd;
SdFile file;
RTC_DS3231 rtc;
DateTime dt;
SCD30 airSensor;
//LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display

const byte sdChipSelect = SS;
const byte WSPEED_PIN   = 2;
const byte DETACH_PIN   = 5;
const byte LED_PIN      = 6;
//const byte LCD_PIN    = 4;

const int arrayLength = 5;
uint32_t unixTime[arrayLength];
uint8_t  windCyc[arrayLength];
uint16_t windDir[arrayLength];
uint16_t concData[arrayLength];
uint8_t  tempData[arrayLength];
uint16_t scdData1;
uint16_t scdData2;

bool wroteNewFile = true;
volatile byte windClicks  = 0;
volatile unsigned long lastWindIRQ = 0;
float WindSpeed;

int VaneValue;
int Direction;
int CalDirection;
#define Offset 0;  


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
  //pinMode(LCD_PIN,    INPUT_PULLUP);
  //lcd.init(); lcd.backlight(); lcd.print("Ready"); delay(1000);
  //lcd.setCursor(0,0); lcd.clear();

  RTCBegin();      delay(2000);
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 6, 3, 23, 7, 0));
  
  SCD30Begin();    delay(2000);
  airSensor.setMeasurementInterval(2);                // # seconds between readings
  airSensor.setAltitudeCompensation(30);              // # meter above sea level
  
  SDBegin();       delay(2000);
  dt = rtc.now();
  CreateNewFile(); delay(2000);
  
  attachInterrupt(digitalPinToInterrupt(WSPEED_PIN), isr_rotation, FALLING);
  interrupts();
  //lcd.clear();
  //lcd.setCursor(0,0);
  
  digitalWrite(LED_PIN, LOW);
  Serial.println("Setup Complete");
}


//---------------MAIN LOOP--------------------//
//---------------------------------------//
void loop() {
  DateTime now_dt = rtc.now();
  for (int i=0; i<arrayLength; i++) {
    dt           = now_dt;
    unixTime[i]  = dt.unixtime();
    windDir[i]   = WindDirection(); 
    CollectGas();
    concData[i]  = scdData1;
    tempData[i]  = scdData2;

    do {
      now_dt = rtc.now();
    } while ( now_dt.unixtime() < dt.unixtime() + 3 );
    
    windCyc[i] = windClicks;
    windClicks = 0;
    //Serial.println("Data Collected");
  }
  WriteSample();




//  if (dt.minute() == 0  && dt.second() == 0) {
//    file.close();
//    CreateNewFile();
//  }

  
  //if (digitalRead(LCD_PIN) == HIGH) lcd.backlight();
  //else lcd.noBacklight();
  //lcd.print(timeUnix);lcd.setCursor(0,1);lcd.print(windDir);lcd.print(',');lcd.print(gasData);lcd.print(',');lcd.print(totalClicks);
  //lcd.clear();
  //lcd.setCursor(0,0);
}

//---------------FILE HANDLING---------------//
//---------------------------------------//
void CreateNewFile() {
  if (digitalRead(DETACH_PIN)) {
    Serial.println("Not creating new file: (DETATCH_PIN HIGH)");
    return;
  }
  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour());
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.sync();
  Serial.println("Created new file: " + String(filename));
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
    bool binary = false;
  
    if (binary == false) {
      String line[arrayLength];
      for (int j=0; j<arrayLength; j++) {
        line[j] = String(unixTime[j])+","+String(windCyc[j])+","+String(windDir[j])+","+String(concData[j])+","+String(tempData[j]);
        file.println(line[j]);
        Serial.println(line[j]);
      }
    }
    else {
      for (int j=0; j<arrayLength; j++) {
        file.write((unixTime[j] >> 24) & 0xFF);
        file.write((unixTime[j] >> 16) & 0xFF);
        file.write((unixTime[j] >> 8)  & 0xFF);
        file.write((unixTime[j] >> 0)  & 0xFF);
        file.write((windCyc[j]>> 0)  & 0xFF);
        file.write((windDir[j]  >> 8)  & 0xFF);
        file.write((windDir[j]  >> 0)  & 0xFF);
        file.write((concData[j]  >> 8)  & 0xFF);
        file.write((concData[j]  >> 0)  & 0xFF);
      }
    }
    file.sync();
    digitalWrite(LED_PIN, LOW);
    //Serial.println("Sample Written");
  }
}


//---------------FUNCTIONS---------------//
//---------------------------------------//
//----------Retrieve Gas Data----------//
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



//----------Retrieve Wind Data----------//
void isr_rotation() {
  if ((unsigned long)( millis() - lastWindIRQ) > 15 ) {
    lastWindIRQ = millis(); 
    windClicks++;           
  }
}

uint16_t WindDirection() {
  VaneValue    = analogRead(A3);
  Direction    = map(VaneValue, 0, 1023, 0, 360);
  CalDirection = Direction + Offset;

  if (CalDirection > 360)
    CalDirection = CalDirection - 360;
  if (CalDirection < 0)
    CalDirection = CalDirection + 360;
  return (CalDirection);
}

//---------------STARTUP MODULES"--------------------//
//----------RTC Begin----------//
void RTCBegin() {
  bool success = false;
  while (success == false) {
    if(rtc.begin()) {
      success = true;
      //lcd.print("RTC OK");
    }
    else {
      Serial.println("RTC Failed");
      //lcd.print("RTC Failed");
    }
    delay(1000); //lcd.clear();
  }
  Serial.println("RTC Operational");
}

//----------Gas Begin----------//
void SCD30Begin() {
  bool success = false;
  while (success == false) {
    if(airSensor.begin(Wire, false)) {
      success = true;
      //lcd.print("Sensor OK");
      }      
    else {
      Serial.println("Sensor Failed");
      //lcd.print("Sensor Failed");
    }
    delay(1000); //lcd.clear();
  }
  Serial.println("Sensor Operational");
}

//----------SD Module Begin ----------//
void SDBegin() {
  bool success = false;
  while (success == false) {
    if(sd.begin(sdChipSelect)) {
      success = true; 
      //lcd.print("SD OK"); 
    }
    else {
      Serial.println("SD Module Failed");
      //lcd.print("SD Failed");
    }
    delay(1000); //lcd.clear();
  }
  Serial.println("SD Module Operational");
}
