int VaneValue;
int Direction;
int CalDirection;
int LastValue;

int WindSensorPin = 2;
volatile unsigned long Rotations;
volatile unsigned long ContactBounceTime;

float WindSpeed;
#define Offset 0;

void setup() {
  LastValue = 1;
  Serial.begin(9600);
  Serial.println("Begin");
  pinMode(WindSensorPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(WindSensorPin), isr_rotation, FALLING);
   
}

void loop() {
  //Wind Direction
  VaneValue = analogRead(A3);
  Direction = map(VaneValue, 0, 1023, 1, 360);
  CalDirection = Direction + Offset;

  if (CalDirection > 360)
    CalDirection = CalDirection - 360;
  if (CalDirection < 1)
    CalDirection = CalDirection + 360;

  //Wind Speed
  Rotations = 0;
  sei();
  delay(1000);
  cli();

  //WindSpeed = Rotations*0.75;

  //Results
  Serial.print(CalDirection);
  //Serial.print(';');
  //Serial.print(float(analogRead(A0)));
  Serial.print(';');
  //Serial.println(WindSpeed);
  Serial.println(Rotations);

}

void isr_rotation () {
  if ((millis() - ContactBounceTime) > 15 ) {
    Rotations ++;
    ContactBounceTime = millis();
  }
}
