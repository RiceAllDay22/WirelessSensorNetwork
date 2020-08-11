//---------------LIBRARIES---------------//
//---------------------------------------//
#include <Wire.h>
#include <LowPower.h>
#include <NDIR_I2C.h>
#include <RTClib.h>
#include <SdFat.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <SoftwareSerial.h>
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display
SoftwareSerial XBee(7, 6); // (rx, tx)

//---------------VARIABLES---------------//
//---------------------------------------//
NDIR_I2C mySensor(0x4D); 
RTC_DS3231 rtc;
SdFat sd;
SdFile file;
DateTime dt;

byte DETACH_PIN = 5, LED_PIN = 4, WSPEED_PIN = 2;
byte sdChipSelect = SS;
uint32_t timeUnix[5];
uint8_t  totalClicks;
uint16_t windDir[5];
uint16_t gasData[5];
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
  Serial.begin(9600);
  Serial.println("Begin");
  pinMode(7, INPUT);
  pinMode(6, OUTPUT);
  pinMode(LED_PIN,     OUTPUT);
  pinMode(DETACH_PIN,  INPUT_PULLUP);
  pinMode(WSPEED_PIN,  INPUT); 
  digitalWrite(LED_PIN,HIGH);

  XBee.begin(9600);
  //lcd.init(); lcd.backlight(); lcd.setCursor(0,0); lcd.clear();
  RTCBegin();      delay(2500);
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 6, 3, 23, 7, 0));
  MHZ16Begin();    delay(5000);
  SDBegin();       delay(2500);
  dt = rtc.now();
  CreateNewFile(); delay(2500);
  
  digitalWrite(LED_PIN, LOW);
  attachInterrupt(digitalPinToInterrupt(WSPEED_PIN), isr_rotation, FALLING);
  interrupts();
}


//---------------LOOP--------------------//
//---------------------------------------//
void loop() {
  for (int i=0; i<1; i++) {
    dt           = rtc.now();
    timeUnix[i]  = dt.unixtime();
    windDir[i]   = WindDirection(); 
    gasData[i]   = CollectGas();
    Serial.print(timeUnix[i]); Serial.print(',');
    Serial.print(windDir[i]);  Serial.print(',');
    Serial.print(gasData[i]);  Serial.print(',');
    Serial.println(windClicks);
    //lcd.print(timeUnix[i]); lcd.setCursor(0,1);
    //lcd.print(windClicks); lcd.print(','); lcd.print(windDir[i]);  lcd.print(','); lcd.print(gasData[i]);

    XBee.write((timeUnix[i] >> 24) & 0xFF);
    XBee.write((timeUnix[i] >> 16) & 0xFF);
    XBee.write((timeUnix[i] >> 8) & 0xFF);
    XBee.write((timeUnix[i] >> 0) & 0xFF); 
    XBee.write((totalClicks >> 0) & 0xFF);
    XBee.write((windDir[i] >> 8) & 0xFF); 
    XBee.write((windDir[i] >> 0) & 0xFF);
    XBee.write((gasData[i] >> 8) & 0xFF); 
    XBee.write((gasData[i] >> 0) & 0xFF);

    while ( rtc.now().unixtime() == dt.unixtime() );
    //lcd.clear();
    //lcd.setCursor(0,0);
  }
  totalClicks = windClicks;
  windClicks  = 0;
  Serial.println(totalClicks);
  //WriteSample();
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

  digitalWrite(LED_PIN, HIGH);
  String line[5];
  for (int j=0; j<5; j++) {
    line[j] = String(timeUnix[j]) + "," + String(totalClicks) + "," + String(windDir[j]) + "," + String(gasData[j]);
    
    //XBee.write((timeUnix[j] >> 24) & 0xFF);
    //XBee.write((timeUnix[j] >> 16) & 0xFF);
    //XBee.write((timeUnix[j] >> 8) & 0xFF);
    //XBee.write((timeUnix[j] >> 0) & 0xFF);
    //XBee.write((totalClicks >> 0) & 0xFF);
    //XBee.write((windDir[j] >> 8) & 0xFF); 
    //XBee.write((windDir[j] >> 0) & 0xFF);
    //XBee.write((gasData[j] >> 8) & 0xFF); 
    //XBee.write((gasData[j] >> 0) & 0xFF);
 
    file.println(line[j]);
  }
  file.sync();
  digitalWrite(LED_PIN, LOW);
  //Serial.println("Sample Written");
}


//---------------FUNCTIONS---------------//
//---------------------------------------//


//----------Retrieve Gas Data----------//
uint16_t CollectGas() {
  uint16_t data;
  if (mySensor.measure())
    data = mySensor.ppm;
  else
    data = 0.0;
  return data;
}



//----------Retrieve Wind Data----------//
void isr_rotation() {
  if ((unsigned long)( millis() - lastWindIRQ) > 15 ) {
    lastWindIRQ = millis(); 
    windClicks++;           
  }
}

uint16_t WindDirection() {
  VaneValue = analogRead(A0);
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
    if(rtc.begin())
      success = true;
    else {
      Serial.println("RTC Failed");
      lcd.print("RTC Failed");
    }
    delay(1000); lcd.clear();
  }
  Serial.println("RTC Operational");
}

//----------Gas Begin----------//
void MHZ16Begin() {
  bool success = false;
  while (success == false) {
    if(mySensor.begin())
      success = true;
    else {
      Serial.println("Sensor Failed");
      lcd.print("Sensor Failed");
    }
    delay(1000); lcd.clear();
  }
  Serial.println("Sensor Operational");
}

//----------SD Module Begin ----------//
void SDBegin() {
  bool success = false;
  while (success == false) {
    if(sd.begin(sdChipSelect))
      success = true;
    else {
      Serial.println("SD Module Failed");
      lcd.print("SD Module Failed");
    }
    delay(1000); lcd.clear();
  }
  Serial.println("SD Module Operational");
}
