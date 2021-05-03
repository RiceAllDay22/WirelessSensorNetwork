#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>

LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
  Serial.begin(9600);
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.print("Ready");
  delay(1000);
  lcd.clear();
}

void loop() {
  delay(50);
  lcd.print(millis()/1000);
  delay(1000);
  lcd.clear();
  delay(50);
}
    
