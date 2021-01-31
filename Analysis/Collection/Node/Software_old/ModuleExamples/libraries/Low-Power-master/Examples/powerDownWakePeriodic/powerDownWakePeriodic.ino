// **** INCLUDES *****
#include "LowPower.h"
#define LED_PIN 2

void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("Begin");
}

void loop() 
{
  Serial.println("Off");
  digitalWrite(LED_PIN, LOW);
  delay(1000);
  // Enter power down state for 8 s with ADC and BOD module disabled
  for (int i = 0; i < 2; i++)
    LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
  Serial.println("On");
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  // Do something here
  // Example: Read sensor, data logging, data transmission.
}
