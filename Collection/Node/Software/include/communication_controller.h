/*Communications Controller.

This file defines a CommunicationsController class that provides acces to communications
functionality, such as sending and recieving data over a wireless network.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
*/

#ifndef COMMUNICATION_CONTROLLER_H
#define COMMUNICATION_CONTROLLER_H


enum class CommunicationModes {
  SIMULATED,
  NRF24L01
};


class CommunicationController {
    private:
    public:
        CommunicationController(CommunicationModes mode);
        bool begin();
};


#endif
