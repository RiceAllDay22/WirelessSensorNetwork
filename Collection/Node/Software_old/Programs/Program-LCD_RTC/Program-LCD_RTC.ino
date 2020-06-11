#include <RTClib.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>


RTC_DS3231 rtc;
DateTime dt;
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display
int WIRE_PIN = 3;


void setup() {
  lcd.init(); // initialize the lcd
  lcd.setCursor(0,0); 
  pinMode(WIRE_PIN, INPUT_PULLUP);
  Serial.begin(9600);
  RTCBegin();
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  rtc.adjust(DateTime(2020, 6, 3, 12, 40, 0));
}

void loop() {
  if (digitalRead(WIRE_PIN) == HIGH) lcd.backlight();
  else lcd.noBacklight();
  dt = rtc.now();
  //Serial.println(dt.unixtime());;
  lcd.print(dt.year(), DEC); lcd.print('/');
  lcd.print(dt.month(), DEC); lcd.print('/');
  lcd.print(dt.day(), DEC); lcd.print(" ");
  lcd.setCursor(0,1);
  lcd.print(dt.hour(), DEC); lcd.print(':');
  lcd.print(dt.minute(), DEC); lcd.print(':');
  lcd.print(dt.second(), DEC);
  lcd.println();
  while (rtc.now().unixtime() == dt.unixtime());
  lcd.setCursor(0,0);
}

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
