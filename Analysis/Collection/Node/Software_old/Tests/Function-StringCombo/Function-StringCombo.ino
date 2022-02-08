String string1 = "File: Hour";
String string2;
String string3 = ".csv";
String string4;

void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 10; i++) {
    string2 = String(i);
    string4 = String(string1 + string2 + string3);
    Serial.println(string4);
    delay(1000);
  }
}
