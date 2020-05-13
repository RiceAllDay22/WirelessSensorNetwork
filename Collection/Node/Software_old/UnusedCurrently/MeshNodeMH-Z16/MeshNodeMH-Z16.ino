#include "RF24.h"
#include "RF24Network.h"
#include "RF24Mesh.h"
#include <SPI.h>
#include <Wire.h>
#include <NDIR_I2C.h>

#define TRANSMIT_PIN   2
#define RECEIVE_PIN    3
#define nodeID 2L

NDIR_I2C mySensor(0x4D);
/**** Configure the nrf24l01 CE and CS pins ****/
RF24 radio(8, 10);
RF24Network network(radio);
RF24Mesh mesh(radio, network);



uint32_t displayTimer = 0;

struct Data {
  uint8_t id;
  unsigned long theTime;
  float theValue;
};

Data data;

struct payload_t {
  unsigned long ms;
  unsigned long counter;
};

void setup() {

  Serial.begin(9600);
  mySensor.begin();
  delay(5000);
  pinMode(TRANSMIT_PIN, OUTPUT);
  pinMode(RECEIVE_PIN, OUTPUT);
  mesh.setNodeID(nodeID);
  Serial.println(F("Connecting to the mesh..."));
  mesh.begin();
  data.id = nodeID;
  randomSeed(analogRead(0));
}



void loop() {

  mesh.update();

  // Send to the master node every second
  if (millis() - displayTimer >= 1000) {
    displayTimer = millis();
    data.theTime = displayTimer;
    if(mySensor.measure())
      data.theValue = mySensor.ppm; 
    if (!mesh.write(&data, 'M', sizeof(data))) { // If a write fails, check connectivity to the mesh network
      if ( ! mesh.checkConnection() ) {//refresh the network address
        Serial.println("Renewing Address");
        if(!mesh.renewAddress()){//If address renewal fails, reconfigure the radio and restart the mesh
          mesh.begin();
        }
      } else {
        Serial.println("Send fail, Test OK");
      }
    } else {
      digitalWrite(TRANSMIT_PIN,HIGH);delay(50);digitalWrite(TRANSMIT_PIN, LOW);delay(50);
      Serial.print("Send OK: "); Serial.println(data.theValue);
    }
  }
if(network.available()){
    RF24NetworkHeader header;
    network.peek(header);
    switch(header.type){
      case 'M': 
        network.read(header,&data,sizeof(data));
        Serial.print(header.from_node); Serial.print(" "); 
        Serial.print(header.to_node); Serial.print(" ");
        Serial.print(header.id); Serial.println("");
        Serial.print(data.id); Serial.print(" "); 
        Serial.print(data.theTime/1000); Serial.print(" ");
        Serial.println(data.theValue); 
        break;
      default: network.read(header,0,0); 
        Serial.print("default");Serial.println(header.type);
        break;
    }
  }
  

//  while (network.available()) {
//    digitalWrite(RECEIVE_PIN,HIGH);
//    delay(50);
//    digitalWrite(RECEIVE_PIN, LOW);    
//    delay(50);
//    RF24NetworkHeader header;
//    payload_t payload;
//    network.read(header, &payload, sizeof(payload));
//    Serial.print("Received packet #");
//    Serial.print(payload.counter);
//    Serial.print(" at ");
//    Serial.println(payload.ms);
//  }
  
}
