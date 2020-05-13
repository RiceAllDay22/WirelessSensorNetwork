/*SD Card Controller.

This file defines a SDCardController class that provides access to SD Card functionality.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef SDCARD_CONTROLLER_H
#define SDCARD_CONTROLLER_H


class SDCardController {
    private: 
    public:
        SDCardController();
        SDCardController(bool simulate);
        bool silumate = false;
};


#endif