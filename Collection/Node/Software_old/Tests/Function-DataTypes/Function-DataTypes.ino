char ch_0 = 48;
char ch_1 = 49;
char ch_2 = 50;
char ch_3 = 51;
char ch_4 = 52; 
char ch_5 = 53;
char ch_6 = 54; 
char ch_7 = 55; 
char ch_8 = 56; 
char ch_9 = 57; 

char char_1[5] = {ch_6, ch_9, ch_6, ch_9, ch_0} ;
char char_2[3] = {ch_4, ch_2, ch_0} ; 

void setup() {
  Serial.begin(9600);
  Serial.println("");
  Serial.println("I've been looking forward to this.");
  Serial.println(ch_1); 
  Serial.println(ch_2);


  int number = 10*(ch_6 - '0') + ch_9 - '0';
  Serial.println(number);
  //for (byte i = 0; i < 5; i++)
    //Serial.print(char_1[i]);
  //Serial.println("");
  //for (byte i = 0; i < 3; i++)
    //Serial.print(char_2[i]);
  
}
 
void loop() {
}
