/*
    Task.h - Library for creating and using task objects for AD7746 sensors.
    Created by Nathaniel Holmes, August 16th 2021.
*/

#include "Arduino.h"

#ifndef Task_h
#define Task_h


class Task
{
  public:
    Task(uint8_t sensorID,uint8_t channelID,uint8_t taskID);
    void executeTask();
    uint8_t _sensorID;
    uint8_t _channelID;
    uint8_t _taskID;
};

#endif