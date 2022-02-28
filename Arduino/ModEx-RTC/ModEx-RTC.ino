// ---------- IMPORT LIBRARIES AND SETUP VARIABLES ----------

#include <RTClib.h>   //Import the RTC library
RTC_DS3231 rtc;       //load an rtc class
DateTime dt;          //Create a variable to store the datetime value


// ---------- MAIN SETUP ----------
void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  RTCBegin();             // Run a user-defined function to start the RTC
  //rtc.adjust(1629385450);                             //Adjust the RTC to a specific unix timestamp
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));     //Adjust the RTC to the local machine's time  
  //rtc.adjust(DateTime(2021, 8, 19, 15, 0, 0));        //Adjust the RTC to a specific datetime (YYYY, MM, DD, hh, mm, ss)
}


// ---------- MAIN CODE ----------
void loop() {
  dt = rtc.now(); 
  Serial.println(dt.unixtime());
  //Wait until the RTC has elapsed 1 second before printing the next timestamp.
  while (rtc.now().unixtime() < dt.unixtime() + 1);
}


// ---------- USER-DEFINED FUNCTION ----------
//This is a function that will try to activate the RTC module.
//If activation fails, it will keep repeating until it works.

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
