//Arduino UNO XBee Transmission Code
#include <SoftwareSerial.h>
#include <SdFat.h>

//SoftwareSerial xbee =  SoftwareSerial(rxPin, txPin);
SoftwareSerial XBee(2, 3);
byte BUTTON_PIN = 5;
byte LED_PIN    = 8;

const uint8_t sdChipSelect = SS;
SdFat sd;
SdFile file;
const size_t LINE_DIM = 50;
char line[LINE_DIM];
size_t n;

uint32_t timeUnix    = 1600013990;
uint8_t  totalClicks = 0;
uint16_t windDir     = 15;
uint16_t gasData     = 520;

 
void setup() {
  Serial.begin(9600); 
  Serial.println("Transmitter");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  XBee.begin(9600);

  //SDBegin();
  Serial.println("Ah yes the negotiator");
}

 
void loop() {
  Serial.println("Sent");

  

  XBee.write((timeUnix >> 24) & 0xFF);
  XBee.write((timeUnix >> 16) & 0xFF);
  XBee.write((timeUnix >> 8) & 0xFF);
  XBee.write((timeUnix >> 0) & 0xFF);

  XBee.write((totalClicks >> 0) & 0xFF);
  
  XBee.write((windDir >> 8) & 0xFF); 
  XBee.write((windDir >> 0) & 0xFF);

  XBee.write((gasData >> 8) & 0xFF); 
  XBee.write((gasData >> 0) & 0xFF);
  
  //XBee.write(data_one);
  delay(1000);
}



//----------File Open----------//
void FileOpen() {
  bool success = false;
  while (success == false) {
    if (file.open("Test.csv", O_READ))
      success = true;
    else
      Serial.println("Card Open Failed");
  } 
  Serial.println("Open Operational");
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
