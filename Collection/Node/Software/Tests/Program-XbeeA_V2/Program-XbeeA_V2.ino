//Arduino UNO XBee Transmission Code
#include <SoftwareSerial.h>
#include <SdFat.h>


SoftwareSerial XBee(2, 3);
byte BUTTON_PIN = 5;

const uint8_t chipSelect = SS;
SdFat sd;
SdFile file;
const size_t LINE_DIM = 50;
char line[LINE_DIM];
size_t n;

 
void setup() {
  Serial.begin(9600); 
  Serial.println("Transmitter");

  if (!sd.begin(chipSelect, SPI_HALF_SPEED)) Serial.println("Begin Fail");
  //if (!file.open("Test.csv", O_READ)) Serial.println("Open Fail");

  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  XBee.begin(9600);
  Serial.println("Ah yes the negotiator");
}
 
void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("Fine collection");
    if (!file.open("Test.csv", O_READ)) { Serial.println("Open Fail"); while(1);}
    while ((n = file.fgets(line, sizeof(line))) > 0) {
      for (byte i = 0; i < strlen(line); i++) { 
        Serial.print(line[i]); 
        XBee.write(line[i]);
        delay(1);
      }
      if (line[n - 1] != '\n') Serial.println(F(" <-- missing nl"));
    }
    //file.sync(); 
    file.close();
  }
  delay(100);
}
