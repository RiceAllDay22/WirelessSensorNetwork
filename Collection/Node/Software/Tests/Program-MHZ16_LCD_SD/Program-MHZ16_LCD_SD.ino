#include <Wire.h>
#include <SD.h>
#include <LiquidCrystal_I2C.h>
#include <NDIR_I2C.h>
#include <SPI.h>

#define BUTTON_PIN 3
#define DELETE_PIN 7
#define SD_PIN 10

File myFile;
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display
NDIR_I2C mySensor(0x4D); //Adaptor's I2C address (7-bit, default: 0x4D)

bool start = false;
float total = 0;
float counter = 0;


void setup()
{
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(DELETE_PIN, INPUT_PULLUP);
  pinMode(SD_PIN, OUTPUT);

  if (SD.begin())
    Serial.println("SD Card ready");
  else
    Serial.println("SD Card failed");

  myFile = SD.open("Data.txt", FILE_WRITE);
  myFile.close();
  
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  if (mySensor.begin()) {
        lcd.print("Wait");
        delay(5000);
  }
  else
      lcd.print("ERROR");
  lcd.clear();
  lcd.print("Ready");
}

void loop()
{
  if (start == false) {
      if (digitalRead(BUTTON_PIN) == LOW)
        start = true;
    }
  
  if (start == true) {
    total = 0;
    counter = 0;
    bool cycle_break = false;
    while (cycle_break == false) {
      lcd.setCursor(0, 1);
      int value;
      if (mySensor.measure()) {
        lcd.clear();
        lcd.setCursor(0,0); delay(50);
        value = mySensor.ppm;
        lcd.print(value); delay(50);
        total += value;
        counter ++;
        lcd.setCursor(0,10); delay(50);
        lcd.print(counter);
        delay(50);
      }
      long theTime = millis()/1000;

      myFile = SD.open("Data.txt", FILE_WRITE);
      if (myFile) {
        //Serial.println(value);
        myFile.print(theTime);
        myFile.print(",");
        myFile.println(value);
        myFile.close();
      }
      else
        Serial.println("Sending Failed");    
      delay(1000);
      if(digitalRead(BUTTON_PIN) == LOW)
        cycle_break = true;
    }
    lcd.clear();
    lcd.setCursor(0,0); delay(50);
    lcd.print("Average: "); delay(50);
    lcd.print(total/counter); delay(50);
    lcd.setCursor(0,10); delay(50);
    lcd.print(counter); delay(50);
    if (cycle_break == true) {
      start = false;
      delay(2500);
    }
    myFile = SD.open("Data.txt");
    if (myFile) {
      Serial.println("Reading File");
      while (myFile.available()) {
        Serial.write(myFile.read());}
      myFile.close();
      Serial.println("File Closed");
    }
  }
  if (digitalRead(DELETE_PIN) == LOW) {
    SD.remove("Data.txt");
    Serial.println("File Removed");
    delay(1000);
  }
}
    
      
