//10-24-2021
byte buf_Read[10];
const int buttonPin = 2;
int buttonState = 0;

void setup() {
  Serial1.begin(9600);
  Serial.begin(9600);
  Serial.println("Begin:9600");
  pinMode(buttonPin, INPUT);
}


//THIS PART WORKS//
void loop() { 
  if (Serial1.available()) {
    Serial1.readBytes(buf_Read, 10);
    Serial.print(buf_Read[0]); Serial.print(",");
    Serial.print(buf_Read[1]); Serial.print(",");
    Serial.print(buf_Read[2]); Serial.print(",");
    Serial.print(buf_Read[3]); Serial.print(",");
    Serial.print(buf_Read[4]); Serial.print(",");
    Serial.print(buf_Read[5]); Serial.print(",");
    Serial.print(buf_Read[6]); Serial.print(",");
    Serial.print(buf_Read[7]); Serial.print(",");
    Serial.print(buf_Read[8]); Serial.print(",");
    Serial.println(buf_Read[9]);
  }
  else {
    
  }
  buttonState = digitalRead(buttonPin);
  if (buttonState == 1) {
    Serial.println("Pressed");
    Serial1.println("Synchronization");
    //delay(1000);
  }
}


//THIS PART WORKS//
//void loop() {
//  if (Serial1.available() > 0){
//    incomingByte = Serial1.read();
//    Serial.print(incomingByte);
//    Serial.print(" ");
//    if(incomingByte == '>') {
//      Serial.println(" ");
//    }
//  }
//  else {
//  }
//}