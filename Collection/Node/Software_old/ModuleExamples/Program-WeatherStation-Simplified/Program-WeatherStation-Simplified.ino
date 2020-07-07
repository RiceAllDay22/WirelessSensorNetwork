/*
 We use A0 for wind direction.
 
 Current:
 130 for 2 seconds while transmitting
 ~30mA during sleep

 Todo:
 Reset after 45 days to avoid millis roll over problems

 What was the wind direction and speed gust for the last 10 minutes?
 Is the 3.3V pin tied on the weather shield or elsewhere?
 */
#include <avr/wdt.h> //We need watch dog for this program
#include <Wire.h> //I2C needed for sensors

// digital I/O pins
const byte WSPEED = 3;
const byte RAIN = 2;
const byte STAT1 = 7;

// analog I/O pins
const byte WDIR = A0;
const byte LIGHT = A1;
const byte BATT = A2;
const byte REFERENCE_3V3 = A3;

//Global Variables
long lastSecond; //The millis counter to see when a second rolls by
unsigned int minutesSinceLastReset; //Used to reset variables after 24 hours. Imp should tell us when it's midnight, this is backup.
byte seconds; //When it hits 60, increase the current minute
byte seconds_2m; //Keeps track of the "wind speed/dir avg" over last 2 minutes array of data
byte minutes; //Keeps track of where we are in various arrays of data
byte minutes_10m; //Keeps track of where we are in wind gust/dir over last 10 minutes array of data

long lastWindCheck = 0;
volatile long lastWindIRQ = 0;
volatile byte windClicks = 0;

//We need to keep track of the following variables:
//Wind speed/dir each update (no storage)
//Wind gust/dir over the day (no storage)
//Wind speed/dir, avg over 2 minutes (store 1 per second)
//Wind gust/dir over last 10 minutes (store 1 per minute)
//Rain over the past hour (store 1 per minute)
//Total rain over date (store one per day)

byte windspdavg[120]; //120 bytes to keep track of 2 minute average
#define WIND_DIR_AVG_SIZE 120
int winddiravg[WIND_DIR_AVG_SIZE]; //120 ints to keep track of 2 minute average
float windgust_10m[10]; //10 floats to keep track of largest gust in the last 10 minutes
int windgustdirection_10m[10]; //10 ints to keep track of 10 minute max
volatile float rainHour[60]; //60 floating numbers to keep track of 60 minutes of rain

//These are all the weather values that wunderground expects:
int winddir; // [0-360 instantaneous wind direction]
float windspeedmph; // [mph instantaneous wind speed]
float windgustmph; // [mph current wind gust, using software specific time period]
int windgustdir; // [0-360 using software specific time period]
float windspdmph_avg2m; // [mph 2 minute average wind speed mph]
int winddir_avg2m; // [0-360 2 minute average wind direction]
float windgustmph_10m; // [mph past 10 minutes wind gust mph ]
int windgustdir_10m; // [0-360 past 10 minutes wind gust direction]
float rainin; // [rain inches over the past hour)] -- the accumulated rainfall in the past 60 min
volatile float dailyrainin; // [rain inches so far today in local time]
//float baromin = 30.03;// [barom in] - It's hard to calculate baromin locally, do this in the agent

//These are not wunderground values, they are just for us
float batt_lvl = 11.8;
float light_lvl = 0.72;

// volatiles are subject to modification by IRQs
volatile unsigned long raintime, rainlast, raininterval, rain;

//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

//Interrupt routines (these are called by the hardware interrupts, not by the main code)
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
void rainIRQ()
// Count rain gauge bucket tips as they occur
// Activated by the magnet and reed switch in the rain gauge, attached to input D2
{
  raintime = millis(); // grab current time
  raininterval = raintime - rainlast; // calculate interval between this and last event

  if (raininterval > 10) // ignore switch-bounce glitches less than 10mS after initial edge
  {
    dailyrainin += 0.011; //Each dump is 0.011" of water
    rainHour[minutes] += 0.011; //Increase this minute's amount of rain

    rainlast = raintime; // set up for next event
  }
}

void wspeedIRQ()
// Activated by the magnet in the anemometer (2 ticks per rotation), attached to input D3
{
  if (millis() - lastWindIRQ > 10) // Ignore switch-bounce glitches less than 10ms (142MPH max reading) after the reed switch closes
  {
    lastWindIRQ = millis(); //Grab the current time
    windClicks++; //There is 1.492MPH for each click per second.
  }
}

void setup()
{
  wdt_reset(); //Pet the dog
  wdt_disable(); //We don't want the watchdog during init

  Serial.begin(9600);

  pinMode(WSPEED, INPUT_PULLUP); // input from wind meters windspeed sensor
  pinMode(RAIN, INPUT_PULLUP); // input from wind meters rain gauge sensor

  pinMode(WDIR, INPUT);
  pinMode(LIGHT, INPUT);
  pinMode(BATT, INPUT);
  pinMode(REFERENCE_3V3, INPUT);

  pinMode(STAT1, OUTPUT);

  midnightReset(); //Reset rain totals

  seconds = 0;
  lastSecond = millis();

  // attach external interrupt pins to IRQ functions
  attachInterrupt(0, rainIRQ, FALLING);
  attachInterrupt(1, wspeedIRQ, FALLING);

  // turn on interrupts
  interrupts();
  Serial.println("Wimp Weather Station online!");
  //reportWeather();

  //  wdt_enable(WDTO_1S); //Unleash the beast
}

void loop()
{
  wdt_reset(); //Pet the dog

  //Keep track of which minute it is
  if(millis() - lastSecond >= 1000)
  {
    lastSecond += 1000;

    //Take a speed and direction reading every second for 2 minute average
    if(++seconds_2m > 119) seconds_2m = 0;

    //Calc the wind speed and direction every second for 120 second to get 2 minute average
    windspeedmph = get_wind_speed();
    winddir = get_wind_direction();
    windspdavg[seconds_2m] = (int)windspeedmph;
    winddiravg[seconds_2m] = winddir;
    //if(seconds_2m % 10 == 0) displayArrays();

    //Check to see if this is a gust for the minute
    if(windspeedmph > windgust_10m[minutes_10m])
    {
      windgust_10m[minutes_10m] = windspeedmph;
      windgustdirection_10m[minutes_10m] = winddir;
    }

    //Check to see if this is a gust for the day
    //Resets at midnight each night
    if(windspeedmph > windgustmph)
    {
      windgustmph = windspeedmph;
      windgustdir = winddir;
    }

    //Blink stat LED briefly to show we are alive
    digitalWrite(STAT1, HIGH);
    //reportWeather(); //Print the current readings. Takes 172ms.
    delay(25);
    digitalWrite(STAT1, LOW);

    //If we roll over 60 seconds then update the arrays for rain and windgust
    if(++seconds > 59)
    {
      seconds = 0;

      if(++minutes > 59) minutes = 0;
      if(++minutes_10m > 9) minutes_10m = 0;

      rainHour[minutes] = 0; //Zero out this minute's rainfall amount
      windgust_10m[minutes_10m] = 0; //Zero out this minute's gust

      minutesSinceLastReset++; //It's been another minute since last night's midnight reset
    }
  }

  //Wait for the imp to ping us with the ! character
  if(Serial.available())
  {
    byte incoming = Serial.read();
    if(incoming == '!')
    {
      //reportWeather(); //Send all the current readings out the imp and to its agent for posting to wunderground. Takes 196ms
      //Serial.print("Pinged!");


    }
    else if(incoming == '@') //Special character from Imp indicating midnight local time
    {
      midnightReset(); //Reset a bunch of variables like rain and daily total rain
      //Serial.print("Midnight reset");
    }
    else if(incoming == '#') //Special character from Imp indicating a hardware reset
    {
      //Serial.print("Watchdog reset");
      delay(5000); //This will cause the system to reset because we don't pet the dog
    }
  }

  //If we go for more than 24 hours without a midnight reset then force a reset
  //24 hours * 60 mins/hr = 1,440 minutes + 10 extra minutes. We hope that Imp is doing it.
  if(minutesSinceLastReset > (1440 + 10))
  {
    midnightReset(); //Reset a bunch of variables like rain and daily total rain
    //Serial.print("Emergency midnight reset");
  }

  delay(100); //Update every 100ms. No need to go any faster.
}

//Prints the various arrays for debugging
void displayArrays()
{
  //Windgusts in this hour
  Serial.println();
  Serial.print(minutes);
  Serial.print(":");
  Serial.println(seconds);

  Serial.print("Windgust last 10 minutes:");
  for(int i = 0 ; i < 10 ; i++)
  {
    if(i % 10 == 0) Serial.println();
    Serial.print(" ");
    Serial.print(windgust_10m[i]);
  }

  //Wind speed avg for past 2 minutes
  /*Serial.println();
   Serial.print("Wind 2 min avg:");
   for(int i = 0 ; i < 120 ; i++)
   {
   if(i % 30 == 0) Serial.println();
   Serial.print(" ");
   Serial.print(windspdavg[i]);
   }*/

  //Rain for last hour
  Serial.println();
  Serial.print("Rain hour:");
  for(int i = 0 ; i < 60 ; i++)
  {
    if(i % 30 == 0) Serial.println();
    Serial.print(" ");
    Serial.print(rainHour[i]);
  }

}

//When the imp tells us it's midnight, reset the total amount of rain and gusts
void midnightReset()
{
  dailyrainin = 0; //Reset daily amount of rain

  windgustmph = 0; //Zero out the windgust for the day
  windgustdir = 0; //Zero out the gust direction for the day

  minutes = 0; //Reset minute tracker
  seconds = 0;
  lastSecond = millis(); //Reset variable used to track minutes

  minutesSinceLastReset = 0; //Zero out the backup midnight reset variable
}

//Calculates each of the variables that wunderground is expecting
void calcWeather()
{
  //current winddir, current windspeed, windgustmph, and windgustdir are calculated every 100ms throughout the day

  //Calc windspdmph_avg2m
  float temp = 0;
  for(int i = 0 ; i < 120 ; i++)
    temp += windspdavg[i];
  temp /= 120.0;
  windspdmph_avg2m = temp;

  //Calc winddir_avg2m, Wind Direction
  //You can't just take the average. Google "mean of circular quantities" for more info
  //We will use the Mitsuta method because it doesn't require trig functions
  //And because it sounds cool.
  //Based on: http://abelian.org/vlf/bearings.html
  //Based on: http://stackoverflow.com/questions/1813483/averaging-angles-again
  long sum = winddiravg[0];
  int D = winddiravg[0];
  for(int i = 1 ; i < WIND_DIR_AVG_SIZE ; i++)
  {
    int delta = winddiravg[i] - D;

    if(delta < -180)
      D += delta + 360;
    else if(delta > 180)
      D += delta - 360;
    else
      D += delta;

    sum += D;
  }
  winddir_avg2m = sum / WIND_DIR_AVG_SIZE;
  if(winddir_avg2m >= 360) winddir_avg2m -= 360;
  if(winddir_avg2m < 0) winddir_avg2m += 360;


  //Calc windgustmph_10m
  //Calc windgustdir_10m
  //Find the largest windgust in the last 10 minutes
  windgustmph_10m = 0;
  windgustdir_10m = 0;
  //Step through the 10 minutes
  for(int i = 0; i < 10 ; i++)
  {
    if(windgust_10m[i] > windgustmph_10m)
    {
      windgustmph_10m = windgust_10m[i];
      windgustdir_10m = windgustdirection_10m[i];
    }
  }

  //Total rainfall for the day is calculated within the interrupt
  //Calculate amount of rainfall for the last 60 minutes
  rainin = 0;
  for(int i = 0 ; i < 60 ; i++)
    rainin += rainHour[i];

}


//Returns the instataneous wind speed
float get_wind_speed()
{
  float deltaTime = millis() - lastWindCheck; //750ms

  deltaTime /= 1000.0; //Covert to seconds

  float windSpeed = (float)windClicks / deltaTime; //3 / 0.750s = 4

  windClicks = 0; //Reset and start watching for new wind
  lastWindCheck = millis();

  windSpeed *= 1.492; //4 * 1.492 = 5.968MPH

  /* Serial.println();
   Serial.print("Windspeed:");
   Serial.println(windSpeed);*/

  return(windSpeed);
}

int get_wind_direction()
// read the wind direction sensor, return heading in degrees
{
  unsigned int adc;

  adc = averageAnalogRead(WDIR); // get the current reading from the sensor

  // The following table is ADC readings for the wind direction sensor output, sorted from low to high.
  // Each threshold is the midpoint between adjacent headings. The output is degrees for that ADC reading.
  // Note that these are not in compass degree order! See Weather Meters datasheet for more information.

  if (adc < 380) return (113);
  if (adc < 393) return (68);
  if (adc < 414) return (90);
  if (adc < 456) return (158);
  if (adc < 508) return (135);
  if (adc < 551) return (203);
  if (adc < 615) return (180);
  if (adc < 680) return (23);
  if (adc < 746) return (45);
  if (adc < 801) return (248);
  if (adc < 833) return (225);
  if (adc < 878) return (338);
  if (adc < 913) return (0);
  if (adc < 940) return (293);
  if (adc < 967) return (315);
  if (adc < 990) return (270);
  return (-1); // error, disconnected?
}


//Takes an average of readings on a given pin
//Returns the average
int averageAnalogRead(int pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0;

  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;

  return(runningValue);
}
