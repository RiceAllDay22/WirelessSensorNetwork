![Python Unit Tests](https://github.com/jkub6/WirelessSensorNetwork/workflows/Python%20Unit%20Tests/badge.svg)
![Node Code Unit Tests](https://github.com/jkub6/WirelessSensorNetwork/workflows/Node%20Code%20Unit%20Tests/badge.svg)
# Wireless Sensor Network

This repository contains the files utilized to create a wireless sensor network to identify, locate, and quantify the presence of C02 in an open field.

Each node utilizes a MZH16 C02 sensor, and a real time clock to take accurate measurements each second. These measurements are stored in microSD card within the node as an hourly file in a binary format. The network periodically propagates all node data to a central hub, where it can be collected on demand.

## Data analysis and visualization
[AnalyzerStep1](Analysis/AnalyzerStep1.ipynb)  
[AnalyzerStep2](Analysis/AnalyzerStep1.ipynb)

## Node Hardware

The board is designed using Autodesk Eagle.

![Node step](Collection/Node/Hardware/Node_step.png)  
![Node schematic](Collection/Node/Hardware/Node_sch.png)  
![Node board](Collection/Node/Hardware/Node_brd.png)  


## Node Software
Code controlling individual nodes is compiled through the Arduino IDE.

Arduino Library Requirments:
 - RTClib
 - SdFat

resources:
[One Drive Resources Folder](https://uofutah-my.sharepoint.com/:f:/g/personal/u1010401_umail_utah_edu/Ekx1kX9h63tNoVFmzbePeowB8LEIOgGHBQhFq369KU12vQ?e=vul3PO)

(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
