//Arduino UNO XBee Transmission Code
#include <SoftwareSerial.h>
#include <SdFat.h>


SoftwareSerial XBee(2, 3);
byte BUTTON_PIN = 5;
byte LED_PIN    = 8;

const uint8_t sdChipSelect = SS;
SdFat sd;
SdFile file;
const size_t LINE_DIM = 50;
char line[LINE_DIM];
size_t n;


void setup() {
  Serial.begin(9600); 
  Serial.println("Transmitter");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  XBee.begin(9600);
  SDBegin();
  Serial.println("Ah yes the negotiator");
}

 
void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("Fine addition");
    if (!file.open("Test.csv", O_READ)) { Serial.println("Open Fail"); return;}
    while ((n = file.fgets(line, sizeof(line))) > 0) {
      for (byte i = 0; i < strlen(line); i++) { 
        Serial.print(line[i]); 
        XBee.write(line[i]);
        //delay(100);
      }
      if (line[n - 1] != '\n') Serial.println(F(" <-- missing nl"));
    }
    file.close();
    Serial.println("My collection");
  }

  while (XBee.available()){
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(LED_PIN, LOW);
    char data = XBee.read();
    Serial.println(data);
  }
  
  delay(100);
}


//----------SD Module Begin ----------//
void SDBegin() {
  bool success = false;
  while (success == false) {
    if(sd.begin(sdChipSelect, SPI_HALF_SPEED))
      success = true;
    else
      Serial.println("SD Module Failed");
    delay(1000);
  }
  Serial.println("SD Module Operational");
}
