//---------------LIBRARIES---------------//
//---------------------------------------//
#include <Wire.h>
#include <SparkFun_SCD30_Arduino_Library.h> 
#include <RTClib.h>
#include <SdFat.h>
#include <LowPower.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display


//---------------VARIABLES---------------//
//---------------------------------------//
SCD30 airSensor;
SdFat sd;
SdFile file;
RTC_DS3231 rtc;
DateTime dt;

byte DETACH_PIN = 5, LCD_PIN = 4, WSPEED_PIN = 2;
byte sdChipSelect = SS;
uint32_t timeUnix;
uint8_t  totalClicks;
uint16_t windDir;
uint16_t gasData;
volatile byte windClicks  = 0;
volatile unsigned long lastWindIRQ = 0;
float WindSpeed;
bool wroteNewFile = true;

int VaneValue;
int Direction;
int CalDirection;
#define Offset 0;

//---------------SETUP-------------------//
//---------------------------------------//
void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("Begin");
  //pinMode(LED_PIN,     OUTPUT);
  pinMode(LCD_PIN, INPUT_PULLUP);
  pinMode(DETACH_PIN,  INPUT_PULLUP);
  pinMode(WSPEED_PIN,  INPUT); 
  //digitalWrite(LED_PIN,HIGH);
  
  //lcd.init(); lcd.backlight(); lcd.print("Ready"); delay(1000);
  //lcd.setCursor(0,0); lcd.clear();
  //Serial.println("Check");
  RTCBegin();      delay(2500);
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 6, 3, 23, 7, 0));
  SCD30Begin();    delay(5000);
  SDBegin();       delay(2500);
  dt = rtc.now();
  CreateNewFile(); delay(2500);
  
  //digitalWrite(LED_PIN, LOW);
  attachInterrupt(digitalPinToInterrupt(WSPEED_PIN), isr_rotation, FALLING);
  interrupts();
  //lcd.clear();
  //lcd.setCursor(0,0);
}


//---------------LOOP--------------------//
//---------------------------------------//
void loop() {
  DateTime now_dt = rtc.now();
  dt              = now_dt;
  timeUnix        = dt.unixtime();
  windDir         = WindDirection(); 

  //if (airSensor.dataAvailable()) {
  //  gasData = airSensor.getCO2();
  //}
  //else
  //  gasData = 0 ;

  while (!airSensor.dataAvailable()) {
  }
  gasData = airSensor.getCO2();

  totalClicks = windClicks;
  windClicks  = 0;

  String line;
  line = String(timeUnix)+","+String(totalClicks)+","+String(windDir)+","+ String(gasData);
  Serial.println(line);  
  //Serial.print(timeUnix); Serial.print(',');
  //Serial.print(windDir);  Serial.print(',');
  //Serial.print(gasData);  Serial.print(',');
  //Serial.println(totalClicks);
  
  //if (digitalRead(LCD_PIN) == HIGH) lcd.backlight();
  //else lcd.noBacklight();
  //lcd.print(timeUnix);lcd.setCursor(0,1);
  //lcd.print(windDir);lcd.print(',');
  //lcd.print(gasData);lcd.print(',');
  //lcd.print(totalClicks);
  //WriteSample();

  //do {
  //  now_dt = rtc.now();
  //} while ( now_dt.unixtime() < dt.unixtime() + 3 );
  
  //lcd.clear();
  //lcd.setCursor(0,0);
}

//---------------FILE HANDLING---------------//
//---------------------------------------//
void CreateNewFile() {
  if (digitalRead(DETACH_PIN)) {
    //Serial.println("Not creating new file: (DETATCH_PIN HIGH)");
    return;
  }
  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour());
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.sync();
  //Serial.println("Created new file: " + String(filename));
}

void WriteSample() {  
  if (digitalRead(DETACH_PIN)) {
    Serial.println("File Closed: (DETATCH_PIN HIGH)");
    //digitalWrite(LED_PIN, HIGH);
    file.close();
    return;
  }

//  digitalWrite(LED_PIN, HIGH);
//  String line[5];
//  for (int j=0; j<5; j++) {
//    line[j] = String(timeUnix[j]) + "," + String(totalClicks) + "," + String(windDir[j]) + "," + String(gasData[j]);
//    file.println(line[j]);
//  }
  String line;
  line = String(timeUnix)+","+String(totalClicks)+","+String(windDir)+","+ String(gasData);   
  file.println(line);
  file.sync();
  Serial.println(line);
//  digitalWrite(LED_PIN, LOW);
//  //Serial.println("Sample Written");
}


//---------------FUNCTIONS---------------//
//---------------------------------------//


//----------Retrieve Gas Data----------//
//uint16_t CollectGas() {
//  uint16_t data;
//  if (mySensor.measure())
//    data = mySensor.ppm;
//  else
//    data = 0.0;
//  return data;
//}



//----------Retrieve Wind Data----------//
void isr_rotation() {
  if ((unsigned long)( millis() - lastWindIRQ) > 15 ) {
    lastWindIRQ = millis(); 
    windClicks++;           
  }
}

uint16_t WindDirection() {
  VaneValue = analogRead(A3);
  Direction = map(VaneValue, 0, 1023, 0, 360);
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
    delay(1000); lcd.clear();
  }
  Serial.println("RTC Operational");
}

//----------Gas Begin----------//
void SCD30Begin() {
  bool success = false;
  while (success == false) {
    if(airSensor.begin()) {
      success = true;
      //lcd.print("Sensor OK");
      }      
    else {
      Serial.println("Sensor Failed");
      //lcd.print("Sensor Failed");
    }
    delay(1000); lcd.clear();
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
    delay(1000); lcd.clear();
  }
  Serial.println("SD Module Operational");
}