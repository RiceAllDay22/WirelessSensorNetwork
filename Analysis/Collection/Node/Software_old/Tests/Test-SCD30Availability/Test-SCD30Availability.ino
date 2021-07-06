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
uint16_t tempData;
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
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  //rtc.adjust(DateTime(2021, 6, 16, 21, 53, 0));
  
  if (airSensor.begin() == false) {
    Serial.println("SCD not detected.");
    while(1);
  }
  airSensor.setMeasurementInterval(2);
  airSensor.setAltitudeCompensation(1300);

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

  do {
    Serial.print(airSensor.dataAvailable());
    delay(0);
    now_dt = rtc.now();
  } while ( now_dt.unixtime() < dt.unixtime() + 3 );
  
  Serial.println("");
  CollectData();
  WriteSample();
  Serial.print("    ");

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
    line = String(timeUnix)+","+String(gasData)+","+String(tempData);
    //file.println(line);
    Serial.println();
    Serial.println(line);
    
    file.sync();
    digitalWrite(LED_PIN, LOW);
  }
}

void CollectData() {
  if (airSensor.dataAvailable()) {
    gasData  = airSensor.getCO2();
    tempData = airSensor.getTemperature();
  }
  else{
    delay(5);
    if (airSensor.dataAvailable()) {
      gasData  = airSensor.getCO2();
      tempData = airSensor.getTemperature();
    }
    else {
      gasData  = 0;
      tempData = 0;
    }
  }
  return;
}
