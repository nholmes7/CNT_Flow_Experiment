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
}
