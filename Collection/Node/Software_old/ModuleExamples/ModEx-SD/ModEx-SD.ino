#include <SdFat.h>

const uint8_t sdChipSelect = SS;

SdFat sd;
SdFile file;

void setup() {
  Serial.begin(9600);
  SDBegin();
  file.open("DATA.csv", O_CREAT|O_WRITE|O_APPEND);
  file.print("UNIXTIME"); file.println("CO2");
  delay(5000);
}

uint32_t counter = 0;

void loop() { 
  file.print(millis()/1000);
  file.print(',');
  file.println(counter);
  file.sync();
  counter ++;
  Serial.println("Done");
  delay(1000);
}


void SDBegin() {
  bool success = false;
  while (success == false) {
    if(sd.begin(sdChipSelect))
      success = true;
    else
      Serial.println("SD Module Failed");
    delay(1000);
  }
  Serial.println("SD Module Operational");
}
