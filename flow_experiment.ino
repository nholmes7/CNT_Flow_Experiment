#include <AD7746.h>
#include <Wire.h>


#define address_0 12           // pin address for multiplexer address 0
#define address_1 11           // pin address for multiplexer address 1
#define address_2 10           // pin address for multiplexer address 2
#define multiplexer_addr 0x70

// Define default register values
#define Cap_Setup_1     0b10000000
#define Cap_Setup_2     0b11000000
#define EXC_Setup       0b00000111
#define Configuration   0b11111001
#define Cap_DAC_A       0b00011100
#define Cap_Offset_H    0x80
#define Cap_Offset_L    0x00

const int message_len = 5;
char message[message_len];
char valid_message[5] = "data";
bool valid = false;
byte result;
uint32_t cap;
uint8_t stat;

// initialize sensor objects
AD7746 sensor1;

void processSerialByte(const byte inByte)
{
  // static variables are only created and initialized the first
  // time the function is called
  static char message [10];
  static unsigned int i = 0;

  message [i++] = inByte;

  switch (inByte)
  {
  case '\r':
    decide(message)
    i = 0;
    // apparently this resets the whol char array?  Need to verify
    message[0] = (char)0;
    break;
  
  default:
    break;
  }
}

char parseCommand(const char message[])
{
  char command[2];
  command[0] = message[1];
  command[1] = message[2];
  return command;
}

void decide(const char message[])
{
  char command[2];
  command = parseCommand(message);
  switch (command)
  {
  case "RC":
    uint32_t reportedCap;
    reportedCap = sensor.getCapacitance();
    break;

  case "RS":
    uint8_t reportedStatus;
    char serialReturnValue[2];
    reportedStatus = sensor.reportStatus();
    serialReturnValue = 
    break;

  case "SC":
    sensor.writeCapSetupRegister(value);
    break;

  case "OM":
    sensor.writeConfigurationRegister(value);
    break;
  
  case "CT":
    sensor.writeConfigurationRegister(value);
    break;
  
  case "CD":
    sensor.writeCapDacARegister(value);
    break;
  
  case "SO":
    // sensor.write
    break;
  
  case "CS":
    break;

  default:
    break;
  }
}

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
  sensor1.writeCapSetupRegister(Cap_Setup_1);
  sensor1.writeExcSetupRegister(EXC_Setup);
  sensor1.writeConfigurationRegister(Configuration);
  sensor1.writeCapDacARegister(Cap_DAC_A);
  
  // set up the multiplexer to communicate over channel 7
  Wire.beginTransmission(multiplexer_addr);
  Wire.write(0b10000000);
  result = Wire.endTransmission();
  if (result) {
    Serial.println(F("Failed to set multiplexer output channel."));
  }
  
}

void loop() {
  stat = sensor1.reportStatus();
  cap = sensor1.getCapacitance();
  
  Serial.print(F("Status byte is: "));
  Serial.println(stat,BIN);
  Serial.print(F("Cap is: "));
  
  Serial.println(cap);
  delay(100);

  while (Serial.available())
  {
    processSerialByte(Serial.read());
  }
}
