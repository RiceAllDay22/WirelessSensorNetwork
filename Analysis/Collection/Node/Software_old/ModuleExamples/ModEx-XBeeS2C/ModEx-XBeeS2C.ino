//10-24-2021
char incomingByte;

void setup() {
  Serial1.begin(9600);
  Serial.begin(9600);
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
