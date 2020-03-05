# Wireless Sensor Network

This repository contains the files utilized to create a wireless sensor network to identify, locate, and quantify the presence of C02 in an open field.

Each node utilizes a MZH16 C02 sensor, and a real time clock to take accurate measurements each second. These measurements are stored in microSD card within the node as an hourly file in a binary format. The network periodically propagates all node data to a central hub, where it can be collected on demand.

## Data analysis and visualization
![Jupyter notebook](Data Analysis/Notebook.ipynb)

## Node Hardware

The board is designed using Autodesk Eagle.

![Sensor node schematic](Node/Node_sch.pdf)  
![Sensor node PCB layout](Node/Node_brd.pdf)

## Node Software
Code controlling individual nodes is compiled through the Arduino IDE.

Arduino Library Requirments:
 - RTClib
 - SdFat

(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
