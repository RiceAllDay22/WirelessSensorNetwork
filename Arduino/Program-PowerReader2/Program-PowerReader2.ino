#include <Wire.h>
#include <RTClib.h>
#include <SdFat.h>
#include <Adafruit_ADS1X15.h>

#define I2C_ADDRESS 0x48
#define BUTTON_PIN 5
#define LED_PIN 8

RTC_DS3231 rtc;
DateTime dt;

SdFat sd;
SdFile file;
const uint8_t sdChipSelect = SS;
Adafruit_ADS1015 ads1115;

int ledState = HIGH;
int buttonState;
int lastButtonState = LOW;

unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

DateTime lastMeasurementTime;
int32_t measurementCounter = 0;

int32_t cumulative_voltage_0_1;
int32_t cumulative_voltage_2_3;

void setup() {
  Serial.begin (9600);
  
  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(LED_PIN, ledState);

  Wire.begin();

  if(!rtc.begin()) Serial.println("RTC setup failed!");
  ads1115.begin();
  if(!sd.begin(sdChipSelect)) Serial.println("SD Card setup failed!");

  dt = rtc.now();
}


void loop() {
  int reading = digitalRead(BUTTON_PIN);

  if (reading != lastButtonState)
    lastDebounceTime = millis();

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState == HIGH)
        ledState = !ledState;
    }
  }

  digitalWrite(LED_PIN, ledState);
  lastButtonState = reading;

  if ((rtc.now()) > lastMeasurementTime) {
    lastMeasurementTime = rtc.now();
    
    int16_t voltage_0_1 = cumulative_voltage_0_1 / measurementCounter;
    int16_t current_0_1 = voltage_0_1 * 4;
    
    int16_t voltage_2_3 = cumulative_voltage_2_3 / measurementCounter;

    
    Serial.println(lastMeasurementTime.unixtime());
    Serial.print(current_0_1 * 3); Serial.println(" mA");
    Serial.print(voltage_2_3 * 3); Serial.println(" mV");
    //Serial.println(cumulative_voltage_0_1);
    //Serial.println(cumulative_voltage_2_3);
    Serial.println("");
    
    cumulative_voltage_0_1 = 0;
    cumulative_voltage_2_3 = 0;
    measurementCounter = 0;
  }

  //cumulative_voltage_0_1 += ads1115.readADC_Differential_0_1();
  cumulative_voltage_0_1 += ads1115.readADC_Differential_2_3();
  delay(10);
  //cumulative_voltage_2_3 += ads1115.readADC_Differential_2_3();
  cumulative_voltage_2_3 += ads1115.readADC_Differential_0_1();
  delay(10);
  measurementCounter++;
  
}
