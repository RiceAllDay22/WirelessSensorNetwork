//---------------LIBRARIES---------------//
#include <Wire.h>
#include <SdFat.h>


//---------------VARIABLES---------------//
byte DETACH_WIRE = 3;
byte LED_PIN     = 2;

SdFat sd;
SdFile file;
DateTime dt;
const uint8_t sdChipSelect = SS;
float gasData;
bool wroteNewFile = true;


//--------------FAST CLOCK--------------//
class FastClock {
  DateTime current;
  long start_unixtime = DateTime(2020, 4, 29, 18, 0, 0).unixtime();
  int count = 0;
  int count2 = 0;

  public:
  FastClock() {
    current = DateTime(start_unixtime);
  }

  bool begin() {
      return true;
  }
  
  DateTime now() {
    current = DateTime(start_unixtime + count);
    
    count2++;
    if (count2 == 3) {
      count2 = 0;
      count++;
    }
    
    return current;
  }
};


//---------------SETUP---------------//
void setup() {
  Serial.begin(9600);
  Serial.println("Begin");
  pinMode(LED_PIN, OUTPUT);
  pinMode(DETACH_WIRE, INPUT_PULLUP);

  FastClock rtc;
  SDBegin();

  dt = rtc.now();
  file = CreateNewFile();
}


//---------------MAIN LOOP---------------//
void loop() {
  while (rtc.now().unixtime() == dt.unixtime());
  float gasData = 1;
  dt = rtc.now();

  WriteSample();
 
  if (dt.minute() == 0 && wroteNewFile == false) {
    wroteNewFile = true;
    file.close();
    CreateNewFile();
  }
  else if (dt.minute() != 0) {
    wroteNewFile = false;
  }
}



//---------------FUNCTIONS---------------//

//----------Create New File----------//
SdFile CreateNewFile() {
  if (digitalRead(DETACH_WIRE)) {
    Serial.println("Not creating new file: (DETATCH_WIRE HIGH)");
    return;
  }

  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(),
          dt.hour());
  
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.println("UNIXTIME,CO2");  // write CSV headers
  Serial.println("Created new file: " + String(filename));
}


//----------Write Data to SD Card----------//
void WriteSample() {  
  if (digitalRead(DETACH_WIRE)) {
    Serial.println("File Closed: (DETATCH_WIRE HIGH)");
    file.close();
    return;
  }
  
  digitalWrite(LED_PIN, HIGH);
  String line = String(dt.unixtime()) + "," + String(gasData);
  file.println(line);
  file.sync();
  digitalWrite(LED_PIN, LOW);
  // Serial.println("Sample Written");
}


//----------SD Module Begin----------//
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
