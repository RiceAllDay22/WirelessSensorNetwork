//Basic Sketch
void setup() {
  //Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  //Serial.println("On");
  digitalWrite(LED_BUILTIN, HIGH);   
<<<<<<< HEAD
  delay(5000);   
  Serial.println("Off");                    
  digitalWrite(LED_BUILTIN, LOW);
  delay(5000);
=======
  delay(10000);   
  //Serial.println("Off");                    
  digitalWrite(LED_BUILTIN, LOW);
  delay(10000);
>>>>>>> 5cbd184ecd221ef8949cf6c71f15da64e79ad9cf
}
//End of Code
