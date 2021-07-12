#include <SdFat.h>

const uint8_t sdChipSelect = SS;
SdFat sd;
SdFile file;

char line;
char C[] = "AT";
int var_a = 2021;
int var_b = 07;
int counter = 0;


void setup() {
  Serial.begin(9600);
  SDBegin();

  char filename[12];
  sprintf(filename, "%04d-%02d.csv", var_a, var_b);  
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.print("UNIXTIME"); file.println("CO2");
  delay(5000); 
} 

void loop() { 

  line = counter;
  //line = char(millis())+","+char(counter) ;
  //file.print(line);
  //file.sync();
  counter ++;

  Serial.println(C);
  //Serial.println(line);
  //Serial.println("Done.");
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
