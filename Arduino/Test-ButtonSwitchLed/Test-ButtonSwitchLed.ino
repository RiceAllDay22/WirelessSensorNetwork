const int BUTTON_PIN = 2;
const int SWITCH_PIN = 3;
const int LED_PIN = 4; 
int buttonState = 0; 

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(SWITCH_PIN), fileclose, FALLING);
}

void loop() {
  Serial.println("Loop");
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);

  buttonState = digitalRead(BUTTON_PIN);
  if (buttonState == HIGH){ 
    Serial.println("Pressed");
  }
  
}


void fileclose() {
  Serial.println("Close");
}
