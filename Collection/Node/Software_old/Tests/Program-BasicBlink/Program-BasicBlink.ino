//Basic Sketch
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  Serial.println("On");
  digitalWrite(LED_BUILTIN, HIGH);   
  delay(5000);   
  Serial.println("Off");                    
  digitalWrite(LED_BUILTIN, LOW);
  delay(5000);
}
//End of Code
