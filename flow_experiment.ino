#include <AD7746.h>
#include <Wire.h>
#include <RingBufCPP.h>
#include <avr/io.h>
#include <avr/interrupt.h>
// #include <Task.h>


#define address_0 12           // pin address for multiplexer address 0
#define address_1 11           // pin address for multiplexer address 1
#define address_2 10           // pin address for multiplexer address 2
#define multiplexer_addr 0x70

// Define default register values
#define Cap_Setup_1     0b10000000
#define Cap_Setup_2     0b11000000
#define EXC_Setup       0b00000111
#define Configuration   0b11000001
#define Cap_DAC_A       0b00011100
#define Cap_Offset_H    0x80
#define Cap_Offset_L    0x00

// Define serial commands
#define RC  1   // read capacitance
#define RS  2   // read status
#define RV  3   // read value
#define OM  4 
#define CT  5
#define CD  6
#define SO  7
#define CS  8
#define AS  9   // activate sensor
#define DS 10   // deactivate sensor

struct sensorReading
{
  uint32_t value;
  uint8_t _sensorID;
  uint8_t _channelID;
  uint32_t timestamp;
};

struct Task
{
  uint8_t sensorID;
  uint8_t channelID;
  uint8_t taskID;
};

// Define buffers and stuff
RingBufCPP<struct sensorReading,5> readingsBuffer;
RingBufCPP<struct Task,20> taskBuffer;
uint8_t messageBuffer[200];

struct Task currentTask;
bool busFree = true;
volatile uint8_t interruptFlag = 0;
uint8_t activeSensors = 0b00000000;
// initialize sensor objects
AD7746 sensor;

void executeTask(struct Task task)
{
  // Reading the capacitance empties the readingsBuffer and does not require 
  // a specific device to be addressed
  if (task.taskID == RC)
  {
    readCapacitance();
    return;
  }

  // Change multiplexer to address the correct device
  uint8_t result;
  Wire.beginTransmission(multiplexer_addr);
  switch (task.sensorID)
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
      Serial.println(F("Invalid multiplexer channel."));
      Wire.endTransmission();
      return;
  }
  result = Wire.endTransmission();
  
  // Multiplexer will return False if operation was successful
  if (result) {
    Serial.println(F("Failed to set multiplexer output channel."));
    return;
  }
  
  // Set the AD7746 channel
  if (task.channelID == 1)
  {
    sensor.writeCapSetupRegister(0b10000000);
  }
  else if (task.channelID == 2)
  {
    sensor.writeCapSetupRegister(0b11000000);
  }
  else
  {
    Serial.println(F("Invalid channel ID."));
    return;
  }

  // Now execute the correct task
  switch (task.taskID)
  {
  case RV:
    readValue(task);
    break;

  case RS:
    readStatus(task);
    break;

  case AS:
    activateSensor(task);
    break;
  
  case DS:
    deactivateSensor(task);
    break;
  // case RC:
  //   setOffset();
  //   break;

  // case RC:
  //   setOpMode();
  //   break;
  
  default:
    Serial.println(F("Invalid taskID."));
    break;
  }
}

/* readCapacitance empties the readingsBuffer.  It pulls the readings one at
a time and assembles the sensorID, channelID, value and timestamp from each
reading into a string of 8-bit ASCII encoded values stored in the messageBuffer
and ready to be sent over serial connection to the connected computer.

Params
    none

Returns
    void
*/
void readCapacitance()
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
    while (readingsBuffer.pull(&reading))
    {
        messageBuffer[i] = reading._sensorID + 48;
        i++;
        messageBuffer[i] = reading._channelID + 48;
        i++;
        ASCIIConvert(reading.value,&messageBuffer[i],6);
        i+=6;
        ASCIIConvert(reading.timestamp,&messageBuffer[i],8);
        i+=8;
    }
    messageBuffer[i] = 59;  // ";" end character
}

void readValue(struct Task task)
{
    uint32_t reportedCap;
    reportedCap = sensor.getCapacitance();
    struct sensorReading currentReading;
    struct sensorReading toDelete;
    currentReading.value = reportedCap;
    currentReading._sensorID = task.sensorID;
    currentReading._channelID = task.channelID;
    currentReading.timestamp = millis();
    if (readingsBuffer.isFull())
    {
        readingsBuffer.pull(&toDelete);
    }
    readingsBuffer.add(currentReading);
}

void readStatus(struct Task task)
{
    uint8_t reportedStatus;
    reportedStatus = sensor.reportStatus();

    messageBuffer[0] = 35;  // "#" start character
    // add 48 to convert to ascii value
    messageBuffer[1] = task.sensorID + 48;
    messageBuffer[2] = task.channelID + 48;
    messageBuffer[3] = reportedStatus + 48;
    messageBuffer[4] = 59;  // ";" end character
}

void activateSensor(struct Task task)
{
  uint8_t sensorBit = 0b00000001;
  sensorBit = sensorBit << ((task.sensorID-1)*2 + task.channelID - 1);
  activeSensors = sensorBit | activeSensors;
  Serial.print(F("Active sensor variable set to "));
  Serial.print(activeSensors,BIN);
  Serial.println(F("."));
}

void deactivateSensor(struct Task task)
{
  uint8_t sensorBit = 0b00000001;
  sensorBit = sensorBit << ((task.sensorID-1)*2 + task.channelID - 1);
  sensorBit = ~sensorBit;
  activeSensors = sensorBit & activeSensors;
  Serial.print(F("Active sensor variable set to "));
  Serial.print(activeSensors,BIN);
  Serial.println(F("."));
}

void processSerialByte(uint8_t inByte)
{
  // static variables are only created and initialized the first
  // time the function is called
  static char message [10];
  static unsigned int i = 0;
  static bool readingMessage  = false;

  if (readingMessage)
  {
    message [i++] = inByte;
  }
  
  switch (inByte)
  {
  case '#':
    // reset the entire message array
    for (int i=0;i<10;i++)
    {
      message[i] = (char)0;
    }
    i = 0;
    readingMessage = true;
    message [i++] = inByte;
    break;
  case ';':
    busFree = true;
    readingMessage = false;
    buildTask(message);
    break;
  
  default:
    break;
  }
}

void buildTask(const char message[10])
{
 struct Task newTask;
 uint8_t taskID = parseCommand(message);
 newTask.taskID = taskID;
 if (taskID != RC)
 {
  uint8_t sensorID = message[3] - 48;
  uint8_t channelID = message[4] - 48;
  newTask.sensorID = sensorID;
  newTask.channelID = channelID;
 }  
 taskBuffer.add(newTask);
}

uint8_t parseCommand(const char message[10])
{
 uint8_t command = 0;
 uint8_t charOne = message[1];
 uint8_t charTwo = message[2];
 if ((charOne == 'R') && (charTwo == 'C'))
 {
   command = RC;
 }
 else if ((charOne == 'R') && (charTwo == 'S'))
 {
   command = RS;
 }
 else if ((charOne == 'R') && (charTwo == 'V'))
 {
   command = RV;
 }
 else if ((charOne == 'A') && (charTwo == 'S'))
 {
   command = AS;
 }
 else if ((charOne == 'D') && (charTwo == 'S'))
 {
   command = DS;
 }
 return command;
}

void writeSerialResponse(uint8_t *response)
{
  while (true)
  {
    Serial.write(*response);
    if (*response == 59)
    {
      break;
    }
    response++;
  }
}

/* ASCIIConvert takes a 32 bit value and converts it to a the ASCII
values representing the characters which define the value in
HEX format.

Params
    value: the 32 bit value defined by the ADC on the AD7746
    *modified: a pointer to the array used to store the ASCII values
        representing the characters in the HEX representation of the
        value
    arraysize: the number of characters in the HEX representaiton of
        the value - 6 for the 24 bit value generated by the AD7746

Returns
    void

Example function call: ASCIIConvert(int value = 0x1234AF,int newvalue[6],6) */
void ASCIIConvert (uint32_t value,uint8_t *modified,int arraySize)
{
 int shiftValue;
 for (int i=0;i<arraySize;i++)
 {
   shiftValue = ((arraySize-1)*4-i*4);
   *modified = ((value & (0b00001111 << shiftValue)) >> shiftValue);
   if (*modified>9)
   {
     *modified += 55;
   }
   else
   {
     *modified += 48;
   }
   modified++;
 }
}

void ISR_4()
{
  if (activeSensors & 0b01000000)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 4;
    newTask.channelID = 1;
    taskBuffer.add(newTask);
  }
  if (activeSensors & 0b10000000)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 4;
    newTask.channelID = 2;
    taskBuffer.add(newTask);
  }
}

void ISR_3()
{
  if (activeSensors & 0b00010000)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 3;
    newTask.channelID = 1;
    taskBuffer.add(newTask);
  }
  if (activeSensors & 0b00100000)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 3;
    newTask.channelID = 2;
    taskBuffer.add(newTask);
  }
}

void ISR_2()
{
  if (activeSensors & 0b00000100)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 2;
    newTask.channelID = 1;
    taskBuffer.add(newTask);
  }
  if (activeSensors & 0b00001000)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 2;
    newTask.channelID = 2;
    taskBuffer.add(newTask);
  }
}

void ISR_1()
{
  if (activeSensors & 0b00000001)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 1;
    newTask.channelID = 1;
    taskBuffer.add(newTask);
  }
  if (activeSensors & 0b00000010)
  {
    struct Task newTask;
    newTask.taskID = RV;
    newTask.sensorID = 1;
    newTask.channelID = 2;
    taskBuffer.add(newTask);
  }
}

void setup() {
  // initiate serial connections
  Serial.begin(9600);
  Wire.begin();
  delay(250);
  
  // set multiplexer address
  pinMode(address_0,OUTPUT);
  pinMode(address_1,OUTPUT);
  pinMode(address_2,OUTPUT);
  digitalWrite(address_0,LOW);
  digitalWrite(address_1,LOW);
  digitalWrite(address_2,LOW);

  // set control registers
  sensor.writeExcSetupRegister(EXC_Setup);
  sensor.writeConfigurationRegister(Configuration);
  // sensor.writeCapDacARegister(Cap_DAC_A);

  // interrupt stuff
  attachInterrupt(4,ISR_4,FALLING);
  attachInterrupt(5,ISR_3,FALLING);
  attachInterrupt(6,ISR_2,FALLING);
  attachInterrupt(7,ISR_1,FALLING);
}

void loop() {
  
  // Receive input from the serial input buffer
  while (Serial.available())
  {
    busFree = false;
    processSerialByte(Serial.read());
  }
  
  // Perform any tasks which may be waiting
  while (taskBuffer.pull(&currentTask))
  {
    executeTask(currentTask);
  }
  
  // Add a message to serial out buffer if one is ready
  if (messageBuffer[0])
  {
    if (busFree)
    {
      writeSerialResponse(&messageBuffer[0]);
      messageBuffer[0] = 0;
    }
  }
}
