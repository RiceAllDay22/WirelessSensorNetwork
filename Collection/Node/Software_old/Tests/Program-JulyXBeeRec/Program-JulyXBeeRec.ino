//Arduino UNO XBee Transmission Code
#include <SoftwareSerial.h>
#include <SdFat.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display
SoftwareSerial XBee(2, 3);

byte DETACH_PIN = 5, LED_PIN = 4;
const uint8_t sdChipSelect = SS;
SdFat sd;
SdFile file;
int incoming[9];

uint32_t timeUnix;
uint8_t  totalClicks;
uint16_t windDir;
uint16_t gasData;
 
void setup() {
  //Serial.begin(9600); 
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(DETACH_PIN, INPUT_PULLUP);
  digitalWrite(LED_PIN,HIGH);

  lcd.init(); lcd.backlight(); lcd.setCursor(0,0); lcd.clear();
  
  XBee.begin(9600);
  SDBegin();
  CreateNewFile();
  digitalWrite(LED_PIN, LOW);
  Serial.println("Begin");
}

 
void loop() {
  byte j = 0;
  while (XBee.available()){
    incoming[j] = XBee.read();
    //Serial.println(incoming[j]);
    j ++;
  }
  
  timeUnix = ( (incoming[0]*16777216) + (incoming[1]*65536) + (incoming[2]*256) + (incoming[3]) ); 
  totalClicks = incoming[4];
  windDir = ( (incoming[5]*256) + incoming[6] );
  gasData = ( (incoming[7]*256) + incoming[8] );
  
  lcd.print(timeUnix); lcd.setCursor(0,1);
  lcd.print(totalClicks); lcd.print(',');
  lcd.print(windDir); lcd.print(',');
  lcd.print(gasData);
  WriteSample();
  //Serial.print(timeUnix); Serial.print(","); Serial.print(totalClicks); Serial.print(","); 
  //Serial.print(windDir); Serial.print(","); Serial.println(gasData);
  //Serial.println("");
  delay(500);
  lcd.clear();
  lcd.setCursor(0,0);
}

 

//----------SD Module Begin ----------//
void SDBegin() {
  bool success = false;
  while (success == false) {
    if(sd.begin(sdChipSelect))
      success = true;
    else {
      Serial.println("SD Module Failed");
      //lcd.print("SD Module Failed");
      //delay(1000); lcd.clear(); lcd.setCursor(0,0);
    }
    delay(1000);
  }
  Serial.println("SD Module Operational");
  //lcd.print("SD Module Operational");
  //delay(1000); lcd.clear(); lcd.setCursor(0,0);
}

void CreateNewFile() {
  //if (digitalRead(DETACH_PIN)) {
    //Serial.println("Not creating new file: (DETATCH_PIN HIGH)");
    //return;
  //}
  file.open("FileTest.csv", O_CREAT|O_WRITE|O_APPEND);
  file.sync();
}

void WriteSample() {
  if (digitalRead(DETACH_PIN)) {
    digitalWrite(LED_PIN, HIGH);
    file.close();
    return;
  }
  //digitalWrite(LED_PIN, HIGH);
  String line;
  line = String(timeUnix) + "," + String(totalClicks) + "," + String(windDir) + "," + String(gasData);
  file.println(line);
  file.sync();
}
