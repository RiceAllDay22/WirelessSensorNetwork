/*C02 Sensor Controller.

This file defines a C02SensorController class that provides access to C02 sensor functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef C02_SENSOR_CONTROLLER_H
#define C02_SENSOR_CONTROLLER_H


class C02SensorController {
    private: 
    public:
        C02SensorController();
        C02SensorController(bool simulate);
        bool silumate = false;
};


#endif
