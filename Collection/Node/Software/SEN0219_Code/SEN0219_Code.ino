int sensorIn = A0;

void setup(){
  Serial.begin(9600);
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
    float Concentration=voltage_diference*50.0/16.0;
    Serial.print(Concentration); Serial.println("ppm");
  }
  delay(100);
}
