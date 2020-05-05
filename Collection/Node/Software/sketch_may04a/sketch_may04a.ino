int value_1 = 5;
int value_2 = 10;
int value_3;

void setup() {
  Serial.begin(9600);
  Serial.println(value_1);
  Serial.println(value_2);
  value_3 = value_1 + value_2;
  Serial.println(value_3);
}

void loop() {
}
