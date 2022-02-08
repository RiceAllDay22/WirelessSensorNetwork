/*Communications Controller.

This file defines a CommunicationsController class that provides acces to communications
functionality, such as sending and recieving data over a wireless network.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef COMMUNICATION_CONTROLLER_H
#define COMMUNICATION_CONTROLLER_H

#include <SoftwareSerial.h>


enum class CommunicationModes {
  FAKE_SERIAL,  // not yet implemented
  NRF24L01,  // not yet implemented
  NONE
};


class CommunicationController {
    private:
        CommunicationModes mode;
    public:
        CommunicationController(CommunicationModes mode);
        bool begin();
        bool sendFiles();
};


#endif
