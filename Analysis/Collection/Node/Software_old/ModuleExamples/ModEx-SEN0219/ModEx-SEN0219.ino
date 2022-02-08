int sensorIn = A0;

void setup(){
  Serial.begin(9600);
  analogReference(DEFAULT);
}

void loop(){
  //Read voltage
  int sensorValue = analogRead(sensorIn);
  float voltage = sensorValue*(5000/1024.0);
  if(voltage == 0)
  {
    Serial.println("Error");
  }
  else if(voltage < 400)
  {
    Serial.println("Pre-heating");
  }
  else
  {
    int voltage_diference = voltage-400;
    float concentration=voltage_diference*50.0/16.0;
    Serial.print(concentration); Serial.println("ppm");
  }
  delay(1000);
}
