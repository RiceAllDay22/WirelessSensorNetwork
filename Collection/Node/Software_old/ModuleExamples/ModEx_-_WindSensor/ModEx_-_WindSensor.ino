#include <Wire.h> //I2C needed for sensors

const byte WSPEED = 3;
const byte WDIR = A0;

long lastWindCheck = 0;
volatile long lastWindIRQ = 0;
volatile byte windClicks = 0;

int winddir; 
float windspeedmph;

void setup() {
  Serial.begin(9600);
  pinMode(WSPEED, INPUT_PULLUP); 
  pinMode(WDIR, INPUT);

  attachInterrupt(1, wspeedIRQ, FALLING);
  interrupts();
}

void loop() {
  
  
  winddir = get_wind_direction();
  Serial.println(winddir);
  delay(1000);
}

void wspeedIRQ() {
// Activated by the magnet in the anemometer (2 ticks per rotation), attached to input D3 
  if (millis() - lastWindIRQ > 10) // Ignore switch-bounce glitches less than 10ms (142MPH max reading) after the reed switch closes
  {
    lastWindIRQ = millis(); //Grab the current time
    windClicks++; //There is 1.492MPH for each click per second.
  }
}



float get_wind_speed() {
  float deltaTime = millis() - lastWindCheck;       //750ms
  deltaTime /= 1000.0;                              //Covert to seconds
  float windSpeed = (float)windClicks / deltaTime;  //3 / 0.750s = 4

  windClicks = 0; //Reset and start watching for new wind
  lastWindCheck = millis();

  windSpeed *= 1.492; //4 * 1.492 = 5.968MPH

  /* Serial.println();
   Serial.print("Windspeed:");
   Serial.println(windSpeed);*/

  return(windSpeed);
}


// WIND DIRECTION


int averageAnalogRead(int pinToRead) {
  byte numberOfReadings     = 10;
  unsigned int runningValue = 0;

  for(int x = 0; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;
  return(runningValue);
}


int get_wind_direction() {
  unsigned int adc;
  adc = averageAnalogRead(WDIR);

  if (adc < 380) return (113);
  if (adc < 393) return (68);
  if (adc < 414) return (90);
  if (adc < 456) return (158);
  if (adc < 508) return (135);
  if (adc < 551) return (203);
  if (adc < 615) return (180);
  if (adc < 680) return (23);
  if (adc < 746) return (45);
  if (adc < 801) return (248);
  if (adc < 833) return (225);
  if (adc < 878) return (338);
  if (adc < 913) return (0);
  if (adc < 940) return (293);
  if (adc < 967) return (315);
  if (adc < 990) return (270);
  return (-1); // error, disconnected?
}
