#include <Wire.h>
#include <RTClib.h>
#include <SdFat.h>
#include <SparkFun_SCD30_Arduino_Library.h>

SdFat sd;
SdFile file;
RTC_DS3231 rtc;
DateTime dt;
SCD30 airSensor;

const byte sdChipSelect = SS;
const byte DETACH_PIN = 5;
const byte LED_PIN    = 6;

uint32_t timeUnix;
uint16_t gasData;
bool wroteNewFile = true;

void setup() {
  Serial.begin(9600);
  Serial.println("SCD30 Example");
  Wire.begin();
  pinMode(DETACH_PIN,   INPUT_PULLUP); 
  pinMode(LED_PIN,      OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  
  if (rtc.begin() == false) {
    Serial.println("RTC not detected.");
    while(1);
  }
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  if (airSensor.begin() == false) {
    Serial.println("SCD not detected.");
    while(1);
  }
  airSensor.setAltitudeCompensation(30);

  if (sd.begin(sdChipSelect) == false) {
    Serial.println("SD not detected.");
    while(1);
  }
  dt = rtc.now();
  CreateNewFile();
  digitalWrite(LED_PIN, LOW);

  
}

void loop() {
  DateTime now_dt = rtc.now();
  dt = now_dt;
  timeUnix = dt.unixtime();
  gasData  = CollectGas();
  
  do {
    now_dt = rtc.now();
  } while ( now_dt.unixtime() < dt.unixtime() + 3 );

  WriteSample();

}

void CreateNewFile() {
  if (digitalRead(DETACH_PIN)) {
    //Serial.println("Not creating new file: (DETATCH_PIN HIGH)");
    return;
  }
  char filename[19];
  sprintf(filename, "%04d-%02d-%02d--%02d.csv", dt.year(), dt.month(), dt.day(), dt.hour());
  file.open(filename, O_CREAT|O_WRITE|O_APPEND);
  file.sync();
  //Serial.println("Created new file: " + String(filename));
}

void WriteSample() {  
  if (digitalRead(DETACH_PIN)) {
    //Serial.println("File Closed: (DETATCH_PIN HIGH)");
    digitalWrite(LED_PIN, HIGH);
    file.close();
    return;
  }

  else {
    digitalWrite(LED_PIN, HIGH);  
    String line;
    line = String(timeUnix)+","+String(gasData);
    file.println(line);
    Serial.println(line);
    
    file.sync();
    digitalWrite(LED_PIN, LOW);
  }
}


uint16_t CollectGas() {
  uint16_t data;
  if (airSensor.dataAvailable()) {
    data = airSensor.getCO2();
  }
  else
    data = 0;
  return data;
}
