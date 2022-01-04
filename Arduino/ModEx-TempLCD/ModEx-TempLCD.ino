#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <OneWire.h> 
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 3
OneWire oneWire(ONE_WIRE_BUS); 
DallasTemperature sensors(&oneWire);
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display
float value;

void setup() {
  //Serial.begin(9600);
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.print("Ready");
  delay(1000);
  lcd.clear();
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  value = sensors.getTempCByIndex(0);
  lcd.print(value);
  delay(950);
  lcd.setCursor(0,0);
}
    
