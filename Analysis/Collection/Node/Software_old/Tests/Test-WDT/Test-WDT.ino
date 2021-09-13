#include <avr/wdt.h>

void setup(){
  Serial.begin(9600);
  Serial.println("Setup started :");
  delay(2000);
  wdt_enable(WDTO_8S);
}


void loop(){
  Serial.println("LOOP started ! ");
  for(int i=0; i<=5; i++){
    Serial.print("Loop : ");
    Serial.print(i);
    Serial.println();
    delay(1000);
    wdt_reset();
  }
  Serial.println("Infinite While");
  while(1){}
}
