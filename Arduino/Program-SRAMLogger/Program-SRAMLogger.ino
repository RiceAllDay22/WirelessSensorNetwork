String test = "this is athis is a test ";
#ifdef __arm__
// should use uinstd.h to define sbrk but Due causes a conflict
extern "C" char* sbrk(int incr);
#else  // __ARM__
extern char *__brkval;
#endif  // __arm__


uint32_t data = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print(data); 
  Serial.print(',');
  Serial.println(freeMemory());
  data ++;
  delay(100);
  
}


int freeMemory() {
  char top;
  #ifdef __arm__
    return &top - reinterpret_cast<char*>(sbrk(0));
  #elif defined(CORE_TEENSY) || (ARDUINO > 103 && ARDUINO != 151)
    return &top - __brkval;
  #else  // __arm__
    return __brkval ? &top - __brkval : &top - __malloc_heap_start;
  #endif  // __arm__
}
