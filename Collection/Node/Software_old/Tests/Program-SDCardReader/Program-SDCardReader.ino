#include <SdFat.h>

const uint8_t chipSelect = SS;
SdFat sd;
SdFile file;
const size_t LINE_DIM = 50;
char line[LINE_DIM];

void setup(void) {
  Serial.begin(9600);
  if (!sd.begin(chipSelect, SPI_HALF_SPEED)) Serial.println("Begin Fail");
  if (!file.open("Test.csv", O_READ)) Serial.println("Open Fail");
  Serial.println("I'll try spinning that's a good trick.");
  
  size_t n;
  while ((n = file.fgets(line, sizeof(line))) > 0) {
    for (byte i = 0; i < strlen(line); i++) { 
      Serial.print(line[i]); 
    }
    if (line[n - 1] != '\n') Serial.println(F(" <-- missing nl"));
  }
}
void loop() {}
