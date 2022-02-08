#include <Wire.h>
#include <LowPower.h>
#include <NDIR_I2C.h>
#include <RTClib.h>
#include <SdFat.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <SoftwareSerial.h>
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display
SoftwareSerial XBee(7, 6); // (rx, tx)


const uint8_t chipSelect = SS;
SdFat sd;
SdFile file;
const size_t LINE_DIM = 50;
char line[LINE_DIM];

void setup(void) {
  Serial.begin(9600);
  pinMode(7, INPUT);
  pinMode(6, OUTPUT);
  XBee.begin(9600);
  
  if (!sd.begin(chipSelect, SPI_HALF_SPEED)) Serial.println("Begin Fail");
  if (!file.open("ThousandLines.csv", O_READ)) {Serial.println("Open Fail");while(1);}
  Serial.println("I'll try spinning that's a good trick.");
  
  size_t n;
  while ((n = file.fgets(line, sizeof(line))) > 0) {
    String Line = line;
    Serial.print(Line);

    int firstCommaIndex  = Line.indexOf(',');
    int secondCommaIndex = Line.indexOf(',', firstCommaIndex+1);
    int thirdCommaIndex  = Line.indexOf(',', secondCommaIndex+1);

    uint32_t timeUnix   = Line.substring(0, firstCommaIndex).toInt();
    uint8_t  windClicks = Line.substring(firstCommaIndex+1, secondCommaIndex).toInt();
    uint16_t windDir    = Line.substring(secondCommaIndex+1, thirdCommaIndex).toInt();
    uint16_t gasData    = Line.substring(thirdCommaIndex+1).toInt();

    //Serial.println(timeUnix);
    //Serial.println(windClicks);
    //Serial.println(windDir);
    //Serial.println(gasData);

    XBee.write((timeUnix >> 24) & 0xFF);
    XBee.write((timeUnix >> 16) & 0xFF);
    XBee.write((timeUnix >> 8) & 0xFF);
    XBee.write((timeUnix >> 0) & 0xFF); 
    XBee.write((windClicks >> 0) & 0xFF);
    XBee.write((windDir >> 8) & 0xFF); 
    XBee.write((windDir >> 0) & 0xFF);
    XBee.write((gasData >> 8) & 0xFF); 
    XBee.write((gasData >> 0) & 0xFF);

    delay(5);
       
  }
  Serial.println("Done");
}
void loop() {}
