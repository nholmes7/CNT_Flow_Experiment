/*
    Task.cpp - Library for creating and using task objects for AD7746 sensors.
    Created by Nathaniel Holmes, August 16th 2021.
*/

#include "Arduino.h"
#include "Task.h"

// Define serial commands
#define RC  1
#define RS  2
#define RV  3
#define OM  4
#define CT  5
#define CD  6
#define SO  7
#define CS  8

Task::Task(uint8_t sensorID,uint8_t channelID,uint8_t taskID)
{
  _sensorID = sensorID;
  _channelID = channelID;
  _taskID = taskID;
}

void Task::executeTask()
{
  // Change multiplexer to correct channel
  uint8_t result;
  Wire.beginTransmission(multiplexer_addr);
  switch (_sensorID)
  {
  case 1:
      Wire.write(0b00010000);
      break;
  case 2:
      Wire.write(0b00100000);
      break;
  case 3:
      Wire.write(0b01000000);
      break;
  case 4:
      Wire.write(0b10000000);
      break;
  default:
      break;
  }
  result = Wire.endTransmission();
  
  if (result) {
    Serial.println(F("Failed to set multiplexer output channel."));
  }
  
  // Set the AD7746 channel
  if (_channelID == 1)
  {
      sensor.writeCapSetupRegister(0b10000000);
  }
  else if (_channelID == 2)
  {
      sensor.writeCapSetupRegister(0b11000000);
  }

  // Now execute the correct task
  switch (_taskID)
  {
  case RC:
    readCapacitance();
    break;

  case RV:
    readValue();
    break;

  case RS:
    readStatus();
    break;

  case RC:
    setOffset();
    break;

  case RC:
    setOpMode();
    break;
  
  default:
    break;
  }
}

void Task::readCapacitance()
{
    struct sensorReading reading;
    // uint16_t bufferSize = readingsBuffer.size();
    // A message consists of a start and end character, with 6 HEX
    // characters representing the value of the capacitance, plus 
    // 2 extra characters for the channel and sensor IDs.
    // uint16_t messageSize = (6+2)*bufferSize + 2;
    // uint8_t message[messageSize];
    messageBuffer[0] = 35;  // "#" start character

    int i = 1;
    while (readingsBuffer.pop(reading))
    {
        messageBuffer[i] = reading._sensorID;
        i++;
        messageBuffer[i] = reading._channelID;
        i++;
        ASCIIConvert(reading.value,&messageBuffer[i],6);
        i+=6;
        ASCIIConvert(reading.timestamp,&messageBuffer[i],8);
        i+=8;
    }
    messageBuffer[i] = 59;  // ";" end character
}

void Task::readValue()
{
    uint32_t reportedCap;
    reportedCap = sensor.getCapacitance();
    struct sensorReading currentReading;
    currentReading.value = reportedCap;
    currentReading._sensorID = _sensorID;
    currentReading._channelID = _channelID;
    currentReading.timestamp = millis();
    readingsBuffer.push(currentReading);
}

void Task::readStatus()
{
    uint8_t reportedStatus;
    reportedStatus = sensor.reportStatus();

    messageBuffer[0] = 35;  // "#" start character
    messageBuffer[1] = _sensorID;
    messageBuffer[2] = _channelID;
    messageBuffer[3] = reportedStatus;
    messageBuffer[4] = 59;  // ";" end character
}

void Task::setOffset()
{
    ;
}

void Task::setOpMode()
{
    ;
}