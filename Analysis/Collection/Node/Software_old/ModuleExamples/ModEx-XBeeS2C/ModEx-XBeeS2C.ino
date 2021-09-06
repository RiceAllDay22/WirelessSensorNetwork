bool started = false;
bool ended = false;
char incomingByte;
byte msg[3];
byte index;
byte response[10];

void setup() {
  Serial1.begin(9600);
  Serial.begin(9600);
  Serial.println("Begin");

}

void loop() {
  while (Serial1.available() > 0){
    //Serial1.readBytes(response, 10);
    incomingByte = Serial1.read();
    Serial.print(incomingByte);
  }
  Serial.println();
  delay(100);

}
