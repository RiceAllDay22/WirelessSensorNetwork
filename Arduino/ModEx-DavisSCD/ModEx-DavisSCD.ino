#include <Wire.h>
#include "SparkFun_SCD30_Arduino_Library.h" 
SCD30 airSensor;

int VaneValue;
int Direction;
int CalDirection;
int LastValue;

int WindSensorPin = 2;
volatile unsigned long Rotations;
volatile unsigned long ContactBounceTime;

float WindSpeed;
#define Offset 0;


void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("SCD30 Example");
  airSensor.begin(); //This will cause readings to occur every two seconds
  LastValue = 1;
  pinMode(WindSensorPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(WindSensorPin), isr_rotation, FALLING);

}

void loop() {

  //Wind Direction
  VaneValue = analogRead(A3);
  Direction = map(VaneValue, 0, 1023, 0, 360);
  CalDirection = Direction + Offset;

  if (CalDirection > 360)
    CalDirection = CalDirection - 360;
  if (CalDirection < 0)
    CalDirection = CalDirection + 360;
  
  //Wind Speed
  WindSpeed = Rotations*0.75;
  Rotations = 0;
  
  Serial.print(WindSpeed);
  Serial.print(';');
  Serial.print(Direction);
  Serial.print(",");
  
  if (airSensor.dataAvailable()) {
    Serial.println(airSensor.getCO2());
  }
  else
    Serial.println("No data");
  delay(3000);
}


void isr_rotation () {
  if ((millis() - ContactBounceTime) > 15 ) {
    Rotations ++;
    ContactBounceTime = millis();
  }
}
