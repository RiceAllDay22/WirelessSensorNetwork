/*Clock Controller.

This file defines a ClockController class that provides access to clock functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef CLOCK_CONTROLLER_H
#define CLOCK_CONTROLLER_H


class ClockController {
    private: 
    public:
        ClockController();
        ClockController(bool simulate);
        bool silumate = false;
};


#endif
