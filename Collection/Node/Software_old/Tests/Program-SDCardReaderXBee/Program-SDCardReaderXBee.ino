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
  if (!sd.begin(chipSelect, SPI_HALF_SPEED)) Serial.println("Begin Fail");
  if (!file.open("TenLines.csv", O_READ)) Serial.println("Open Fail");
  Serial.println("I'll try spinning that's a good trick.");
  
  size_t n;
  while ((n = file.fgets(line, sizeof(line))) > 0) {
    for (byte i = 0; i < strlen(line); i++) { 
      Serial.print(line[i]); 
    }
    if (line[n - 1] != '\n') Serial.println(F(" <-- missing nl"));
  }
}
void loop() {}
