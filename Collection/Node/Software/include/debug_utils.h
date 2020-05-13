/*Debugging Utilities.

This file provides utility functions for debugging. Most will only be enabled upon defining the
DEBUG preprocessor command.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef DEBUG_UTILS_H
#define DEBUG_UTILS_H


#ifdef DEBUG
    #include <Arduino.h>

    bool DEBUG_INITIALIZED = false;

    #ifndef BAUD_RATE
        #define BAUD_RATE 9600
    #endif
    
    #define DEBUG_INIT() {\
        extern bool DEBUG_INITIALIZED;\
        if(!DEBUG_INITIALIZED) {\
            DEBUG_INITIALIZED = true;\
            Serial.begin(BAUD_RATE);\
        }\
    }

    #define DEBUG_PRINT(str) {\
        Serial.print(millis());\
        Serial.print(": ");\
        Serial.print(__PRETTY_FUNCTION__);\
        Serial.print(' ');\
        Serial.print(__FILE__);\
        Serial.print(':');\
        Serial.print(__LINE__);\
        Serial.print(' ');\
        Serial.println(str);\
    }

#else
   #define DEBUG_INIT()
   #define DEBUG_PRINT(str)
#endif


#endif
