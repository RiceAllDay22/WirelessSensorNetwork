int sensorIn = A7;

void setup(){
  Serial.begin(9600);
  SEN0219Begin();
}

void loop(){
  uint16_t GasData = CollectGas();
  Serial.println(GasData);
  delay(1000);
}



void SEN0219Begin() {
  analogReference(DEFAULT);
  int sensorValue_in = analogRead(sensorIn);
  float voltage_in = sensorValue_in*(5000/1024.0);
  
  bool success = false;
  while (success == false) {
    if(voltage_in > 400)
      success = true;
    else
      Serial.println("Pre-Heating");
    delay(1000);
  }
  Serial.println("Sensor Operational");
}



uint16_t CollectGas() {
  analogReference(DEFAULT);
  int sensorValue = analogRead(sensorIn);
  float voltage = sensorValue*(5000/1024.0);
  uint16_t data = (voltage-400)*50.0/16.0;
  return data;
}
