#include <SPI.h>        //Call SPI library so you can communicate with the nRF24L01+
#include <nRF24L01.h>   //nRF2401 libarary found at https://github.com/tmrh20/RF24/
#include <RF24.h>

#include <Wire.h>
#include <NDIR_I2C.h>
#include "RTClib.h"

NDIR_I2C mySensor(0x4D);
RTC_DS3231 rtc;
uint32_t unixxtime;

const uint8_t pinCE  = 8;                   //This pin is used to set the nRF24 to standby (0) or active mode (1)
const uint8_t pinCSN = 10;                   //This pin is used to tell the nRF24 whether the SPI communication is a command
RF24 wirelessSPI(pinCE, pinCSN);            // Declare object from nRF24 library (Create your wireless SPI)
const uint64_t wAddress = 0xB00B1E50C3LL;   //Create pipe address to send data, the "LL" is for LongLong type

const uint8_t rFChan = 89;                  //Set channel default (chan 84 is 2.484GHz to 2.489GHz)
const uint8_t rDelay = 7;                   //this is based on 250us increments, 0 is 250us so 7 is 2 ms
const uint8_t rNum   = 5;  

struct PayLoad {
  float value;
  uint32_t clockTime;
};
PayLoad payload; //create struct object

void setup() {
  Serial.begin(9600);
  if (mySensor.begin())
    Serial.println("Sensor Works");
  delay(1000);
  wirelessSPI.begin();  //Start the nRF24 module
  wirelessSPI.setChannel(rFChan);
  wirelessSPI.setRetries(rDelay, rNum);   //if a transmit fails to reach receiver (no ack packet) then this sets retry attempts and delay between retries
  wirelessSPI.openWritingPipe(wAddress);  //open writing or transmit pipe
  wirelessSPI.stopListening();            //go into transmit mode
  randomSeed(analogRead(0));
}

void loop() {
  delay(1000);
  DateTime now = rtc.now();
  unixxtime = now.unixtime();

  if (mySensor.measure()) {
    payload.value = mySensor.ppm;
    payload.clockTime = unixxtime;
    Serial.println(mySensor.ppm);
    Serial.println(unixxtime);
  }
  
  if (!wirelessSPI.write(&payload, sizeof(payload))) { //send data and remember it will retry if it fails
    Serial.println("Bad");
    delay(random(5, 20)); //as another back up, delay for a random amount of time and try again
    if (!wirelessSPI.write(&payload, sizeof(payload))) {
    }
  }
  else
    Serial.println("Good"); 
}
