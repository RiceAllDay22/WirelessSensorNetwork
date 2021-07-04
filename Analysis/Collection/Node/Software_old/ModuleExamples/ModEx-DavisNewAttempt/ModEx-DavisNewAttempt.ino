int VaneValue;
int Direction;
int CalDirection;
int LastValue;

int WindSensorPin = 2;
int WindAnalogPin = A0;
float WindSpeed;
float WindAnalog;
#define Offset 0;

void setup() {
  LastValue = 1;
  Serial.begin(9600);
  Serial.println("Begin");
  pinMode(WindSensorPin, INPUT);
   
}

void loop() {
  //Wind Direction
  VaneValue = analogRead(A3);
  Direction = map(VaneValue, 0, 1023, 0, 360);
  CalDirection = Direction + Offset;

  if (CalDirection > 360)
    CalDirection = CalDirection - 360;
  if (CalDirection < 0)
    CalDirection = CalDirection + 360;

  //Wind Speed
  WindSpeed = digitalRead(WindSensorPin);
  WindAnalog = analogRead(WindAnalogPin);

  //Results
  Serial.print(CalDirection);
  Serial.print(';');
  Serial.println(WindAnalog);
  //Serial.println(WindSpeed);

  delay(1000);
}
