#define LED_PIN LED_BUILTIN

void setup() {
  pinMode(LED_PIN, OUTPUT);
  for (int i = 0; i < 20; i++){
    if(i != 2)
    pinMode(i, OUTPUT); 
  }
  //attachInterrupt(0, digitalInterrupt, FALLING);

  WDTCSR = (24);
  WDTCSR = (33);
  WDTCSR |= (1<<6);
  
  //Disable ADC Analog to DIgital converter
  ADCSRA &= -(1<<7);

  //ENABLE SLEEP
  SMCR |= (1<<2);
  SMCR |= 1;
  
}

void loop() {
  //digitalWrite(LED_PIN, HIGH);
  //delay(1000);   
  //digitalWrite(LED_PIN, LOW);
  //delay(1000);



  for (int i = 0; i < 1; i++){
  //BOD DISABLE
  MCUCR |= (3<<5);
  MCUCR = (MCUCR & ~(1<<5)) | (1<<6);
  __asm__ __volatile__("sleep");
  }
}

ISR(WDT_vect){}
//void digitalInterrupt(){
  //}
