bool started = false;
bool ended = false;
//10-24-2021

char incomingByte;
byte msg[3];
byte index;
//byte response[10];

void setup() {
  Serial1.begin(9600);
  Serial.begin(9600);
  Serial.println("Begin");

}

void loop() {
  if (Serial1.available() > 0){
    incomingByte = Serial1.read();
    Serial.print(incomingByte);
    if(incomingByte == '>') {
      Serial.println("");
    }
  }
  else {
    //Serial.println("None");
  }
  //Serial.println();
  //delay(100);

}
