//---------------LIBRARIES---------------//
#include <Wire.h>
#include <LowPower.h>
#include <NDIR_I2C.h>
#include <RTClib.h>
#include <SdFat.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>

LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display



//---------------VARIABLES---------------//
NDIR_I2C mySensor(0x4D); 
RTC_DS3231 rtc;
SdFat sd;
SdFile file;
DateTime dt;

byte DETACH_PIN = 5, LED_PIN = 4, WSPEED_PIN = 3, WDIR_PIN = A0;
const uint8_t sdChipSelect = SS;
uint32_t timeUnix;
uint8_t  totalClicks;
uint8_t  windDir;
uint16_t gasData;
volatile byte windClicks  = 0;
volatile long lastWindIRQ = 0;
bool wroteNewFile = true;


//---------------SETUP---------------//
void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  pinMode(LED_PIN,    OUTPUT);
  pinMode(DETACH_PIN, INPUT_PULLUP);
  pinMode(WSPEED_PIN, INPUT_PULLUP); 
  pinMode(WDIR_PIN,   INPUT);
  digitalWrite(LED_PIN,HIGH);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.clear();



  RTCBegin();      delay(2500);
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2020, 6, 3, 23, 7, 0));
  //Serial.println("TimeSet"); 
  MHZ16Begin();    delay(5000);
  SDBegin();       delay(2500);
  dt = rtc.now();
  CreateNewFile(); delay(2500);
  
  digitalWrite(LED_PIN, LOW);
  attachInterrupt(1, wspeedIRQ, FALLING);
  interrupts();
}


//---------------MAIN LOOP---------------//
void loop() {
  dt = rtc.now();
  timeUnix  = dt.unixtime();
  windDir   = WindDirection(); 
  gasData   = CollectGas();
  lcd.print(totalClicks); lcd.print(',');
  lcd.print(windDir);    lcd.print(',');
  lcd.print(gasData);
  //Serial.print(timeUnix);    Serial.print(",");
  //Serial.print(totalClicks); Serial.print(",");
  //Serial.print(windDir);     Serial.print(",");
  //Serial.println(gasData);
  WriteSample();  
  
  if (dt.minute() == 0 && wroteNewFile == false) {
    wroteNewFile = true;
    file.close();
    CreateNewFile();
  }
  else if (dt.minute() != 0) {
    wroteNewFile = false;
  }

  while ( rtc.now().unixtime() == dt.unixtime() );
  lcd.clear();
  totalClicks = windClicks;
  windClicks  = 0;
}


//---------------FUNCTIONS---------------//

//----------Create New File----------//
void CreateNewFile() {
  if (digitalRead(DETACH_PIN)) {
    Serial.println("Not creating new file: (DETATCH_PIN HIGH)");
    return;
  }
  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour());
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  //file.println("UNIXTIME,CO2");
  file.sync();
  Serial.println("Created new file: " + String(filename));
}

//----------Write Data to SD Card----------//
void WriteSample() {  
  if (digitalRead(DETACH_PIN)) {
    Serial.println("File Closed: (DETATCH_PIN HIGH)");
    digitalWrite(LED_PIN, HIGH);
    file.close();
    return;
  }
  //String line = String(timeUnix) + "," + String(gasData);
  //file.println(line);
  file.write((timeUnix >> 24) & 0xFF); file.write((timeUnix >> 16) & 0xFF); file.write((timeUnix >> 8) & 0xFF); file.write((timeUnix >> 0) & 0xFF);
  file.write((totalClicks >> 0) & 0xFF);
  file.write((windDir >> 0) & 0xFF);
  file.write((gasData >> 8) & 0xFF); file.write((gasData >> 0) & 0xFF);
  file.sync();
  //file.close();
  //digitalWrite(LED_PIN, LOW);
  //Serial.println("Sample Written: " + String(GasData));
}

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
void wspeedIRQ() {
  if ((unsigned long)( millis() - lastWindIRQ) > 10 ) {
    lastWindIRQ = millis(); 
    windClicks++;           
  }
}

int averageAnalogRead(int pinToRead) {
  byte numberOfReadings     = 10;
  unsigned int runningValue = 0;

  for(int x = 0; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;
  return(runningValue);
}

uint8_t WindDirection() {
  unsigned int adc = averageAnalogRead(WDIR_PIN);
  if (adc < 1)   return(-1);
  if (adc < 380) return (5); //113
  if (adc < 393) return (3);  //68
  if (adc < 414) return (4);  //90
  if (adc < 456) return (7); //158
  if (adc < 508) return (6); //135
  if (adc < 551) return (9); //203
  if (adc < 615) return (8); //180
  if (adc < 680) return (1);  //23
  if (adc < 746) return (2);  //45
  if (adc < 801) return (11); //248
  if (adc < 833) return (10); //225
  if (adc < 878) return (15); //338
  if (adc < 913) return (0);  //0
  if (adc < 940) return (13); //293
  if (adc < 967) return (14); //315
  if (adc < 990) return (12); //270
  return (-1);
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
