/*Debugging Utilities.

This file provides utility functions for debugging. Most will only be enabled upon defining the
DEBUG preprocessor command.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef DEBUG_UTILS_H
#define DEBUG_UTILS_H


#ifdef DEBUG_MESSAGES
    #include <Arduino.h>

    #ifndef BAUD_RATE
        #define BAUD_RATE 9600
    #endif
    
    #define DEBUG_INIT() {\
        Serial.begin(BAUD_RATE);\
        while(!Serial);\
        Serial.println("Debug initialized");\
    }

    #define DEBUG_PRINT(str) {\
        Serial.print('<');\
        Serial.print(millis());\
        Serial.print(": ");\
        Serial.print(__PRETTY_FUNCTION__);\
        Serial.print(' ');\
        Serial.print(__FILE__);\
        Serial.print(':');\
        Serial.print(__LINE__);\
        Serial.print(">: ");\
        Serial.println(str);\
    }

#else
   #define DEBUG_INIT()
   #define DEBUG_PRINT(str)
#endif


#endif
