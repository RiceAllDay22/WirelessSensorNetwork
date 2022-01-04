#include <SPI.h>          //Call SPI library so you can communicate with the nRF24L01+
#include <nRF24L01.h>     //nRF2401 libarary found at https://github.com/tmrh20/RF24/
#include <RF24.h> 

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>

const uint8_t pinCE   = 8;                  //This pin is used to set the nRF24 to standby (0) or active mode (1)
const uint8_t pinCSN  = 10;                 //This pin is used for SPI comm chip select
RF24 wirelessSPI(pinCE, pinCSN);            // Declare object from nRF24 library (Create your wireless SPI) 
const uint64_t rAddress = 0xB00B1E50C3LL;   //Create pipe address for the network the "LL" is for LongLong type
const uint8_t rFChan = 89;       

struct PayLoad {
  float value;
  uint32_t clockTime;
};

PayLoad payload;
LiquidCrystal_I2C lcd(0x27, 16,2);

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.print("Ready");
  delay(1000);
  lcd.clear();
  
  wirelessSPI.begin();                      //Start the nRF24 module
  wirelessSPI.setChannel(rFChan);           //set communication frequency channel
  wirelessSPI.openReadingPipe(1,rAddress);  //This is receiver or master so we need to be ready to read data from transmitters
  wirelessSPI.startListening();             // Start listening for messages            
}

void loop() {
  if(wirelessSPI.available()){ //Check if recieved data
     wirelessSPI.read(&payload, sizeof(payload)); //read packet of data and store it in struct object
     Serial.println(payload.value);
     Serial.println(payload.clockTime);
     Serial.println();
  }
  lcd.print(payload.value);
  lcd.setCursor(0,1);
  lcd.print(payload.clockTime);
  delay(900);
  lcd.clear();
  delay(100);
  
}
