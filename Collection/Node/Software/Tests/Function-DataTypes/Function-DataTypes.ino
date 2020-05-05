//char ch_0 = 48; // 6
//char ch_1 = 49; // 9
char ch_2 = 50; // 6
//char ch_3 = 51; // 9
char ch_4 = 52; // 6
//char ch_5 = 53; // 9
char ch_6 = 54; // 6
//char ch_7 = 55; // 6
//char ch_8 = 56; // 9
char ch_9 = 57; // 9

char char_1[1][2] = {ch_6, ch_9} ;
//char char_2[3] = {ch_4, ch_2, ch_0} ; 

void setup() {
  Serial.begin(9600);
  Serial.println("I've been looking forward to this.");
  //Serial.println("");
  //Serial.println(value_1);
  //Serial.println(value_2);
  //Serial.println(value_3);
  //Serial.println(ch_1);
  Serial.println(ch_4); 
  Serial.println(ch_2);
  Serial.println(char_1);
  //Serial.println("");
  //Serial.println(char_2);
  
}
 
void loop() {
}
