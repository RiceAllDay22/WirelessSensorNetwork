/*
  ---------- PLEASE READ BEFORE STARTING ----------
  
  Guide for Reading Data from LI-800 Sensor via Analog Pin
  By:       Adriann Liceralde
  For:      Carbon Science Research at the University of Utah
  License:  MIT (basically do whatever you want with this code)
  Date:     July 29, 2021
  
INTRODUCTION
  This code is for collecting CO2 data from a GasHound LI-800.
  The Arduino will use an analog pin to read the "CO2 V OUT" of the LI-800.
  This code follows Section 3-27 to 3-30 of the Instruction Manual.

IMPORTANT NOTES
  Refer to the Instruction Manual for additional information about the LI-800.

WIRING
  Arduino     LI-800
  ------------------
  A0 Pin  ->  TERMINAL #9  (CO2 V OUT)
  GND Pin ->  TERMINAL #10 (GND)

CALIBRATION

SPECIFCATIONS

LINKS

CONTACT
  Email any questions or concerns to adriann8399@gmail.com
 */
#include <RTClib.h>
RTC_DS3231 rtc;
DateTime dt;
DateTime now_dt;
uint32_t now_ut;

const int DAC_OFFSET = 25;        //According to the manual, the DAC offset for this device is 25 ppm
void setup() {
  Serial.begin(9600);             //Activates the Serial port and sets the baud rate of the Serial Monitor. 9600 is the common rate
  if(rtc.begin() == false) {
    Serial.println("RTC Failed");
    while (1);
  }
}

void loop() {
  dt = rtc.now(); 
  int A0_Value  = analogRead(A0);                   //The analogRead() function will read the value coming from an analog pin, in this case, pin A0
  
  float    V_Out     = A0_Value*(5.0/1023.0);       //This will convert the analog value into a voltage value  
  float    gasConc   = V_Out*2000/5 - DAC_OFFSET;   //This will convert the voltage value to a concentration according to Equation 3-6 of the Instruction Manual 
  
  Serial.print(dt.unixtime());                                 //Print the time, in seconds
  Serial.print(", ");
  Serial.print(A0_Value);                           //Print the Analog reading outputted by the LI-800 device
  Serial.print(", ");
  Serial.println(gasConc);                          //Print the co2 concentration
  do {
    now_dt = rtc.now();
    now_ut = now_dt.unixtime();
    delay(50);
  }
  while (now_ut < dt.unixtime() + 1);
}
