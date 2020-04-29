//Basic Sketch
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  Serial.println("Ah yes the negotiator");
  digitalWrite(LED_BUILTIN, HIGH);   
  delay(1000);                       
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("These fill make a fine addition to my collection");
  delay(1000);
}
//End of Code
