//Arduino UNO XBee Transmission Code
#include <SoftwareSerial.h>
#include <SdFat.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
LiquidCrystal_I2C lcd(0x27,16,2); // set the LCD address to 0x27 for a 16 chars and 2 line display


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

uint32_t timeUnix[5];
uint8_t  totalClicks[5];
uint16_t windDir[5];
uint16_t gasData[5];
 
void setup() {
  Serial.begin(9600); 
  Serial.println("Transmitter");
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.clear();
  
  XBee.begin(9600);
  //SDBegin();
  //Serial.println("Ah yes the negotiator");
}

 
void loop() {
  //Serial.println("Nothing");
  byte j = 0;
  bool calc = false;
  int incoming[9];
  while (XBee.available()){
    incoming[j] = XBee.read();
    //Serial.println(incoming[j]);
    j ++;
    calc = true;
  }
  //Serial.println("Done");
  if (calc == true) {
    timeUnix[0]    = ( (incoming[0]*16777216) + (incoming[1]*65536) + (incoming[2]*256) + (incoming[3]) ); 
    totalClicks[0] = incoming[4];
    windDir[0]     = ( (incoming[5]*256) + incoming[6] );
    gasData[0]     = ( (incoming[7]*256) + incoming[8] );
    Serial.print(timeUnix[0]); Serial.print(","); Serial.print(totalClicks[0]); Serial.print(","); 
    Serial.print(windDir[0]); Serial.print(","); Serial.println(gasData[0]);
    Serial.println("");
    //lcd.print(timeUnix); lcd.setCursor(0,1);
    //lcd.print(totalClicks); lcd.print(',');
    //lcd.print(windDir); lcd.print(',');
    //lcd.print(gasData);
    //delay(1000);
    //lcd.clear();
    //lcd.setCursor(0,0);
  } 
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