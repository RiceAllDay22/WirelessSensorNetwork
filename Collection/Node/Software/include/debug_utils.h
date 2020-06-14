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
    #define DEBUG_PRINT(x) Serial.print(x);
    #define DEBUG_PRINTLN(x) Serial.println(x);
#else
    #define DEBUG_PRINT(x)
    #define DEBUG_PRINTLN(x)
#endif

#endif
