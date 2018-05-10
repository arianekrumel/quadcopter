/*
 * FlightController
 * 
 * This is an Arduino application that connects with
 * controller through receiver system
 * 
 * The circuit:
 * * Arduino Mega2560
 * * Fly Sky FS-T6 Controller
 * * Fly Sky FS-R6B
 * 
 * 5/6/18
 * Ariane Krumel
 * 
 * 
 * Based on https://www.youtube.com/watch?v=v_N5HmXmDyk
 */

int pinRoll   = 0; // Channel 1
int pinPitch  = 1; // Channel 2
int pinThrust = 2; // Channel 3
int pinYaw    = 3; // Channel 4

unsigned long rawData   = 0;
unsigned long rawRoll   = 0;
unsigned long rawPitch  = 0;
unsigned long rawThrust = 0;
int rawYaw    = 0;
int mappedData = 0;
char trim;

void setup() {
  delay(1000);
  pinMode(pinRoll, INPUT);
  pinMode(pinPitch, INPUT);
  pinMode(pinThrust, INPUT);
  pinMode(pinYaw, INPUT);
  Serial.begin(9600);

  rawRoll = pulseIn(pinRoll, HIGH, 25000);
  rawPitch = pulseIn(pinPitch, HIGH, 25000);
  rawThrust = pulseIn(pinThrust, HIGH, 25000);
  rawYaw = pulseIn(pinYaw, HIGH, 25000);
}

void loop() {
  rawData = pulseIn(pinRoll, HIGH, 25000);
  trim = (rawData < rawRoll) ? '-' : '+';
  if(rawData != rawRoll)
  {
    Serial.print("Roll (");
    Serial.print(trim);
    Serial.print("): ");
    mappedData = map(rawData, 1530, 2000, 0, 255);
    Serial.println(mappedData);
    rawRoll = rawData;
  }

  rawData = pulseIn(pinPitch, HIGH, 25000);
  trim = (rawData < rawPitch) ? '-' : '+';
  if(rawData != rawPitch)
  {
    Serial.print("Pitch (");
    Serial.print(trim);
    Serial.print("): ");
    mappedData = map(rawData, 1530, 2000, 0, 255);
    Serial.println(mappedData);
    rawPitch = rawData;
  }

  rawData = pulseIn(pinYaw, HIGH, 25000);
  trim = (rawData < rawYaw) ? '-' : '+';
  if(rawData != rawYaw)
  {
    Serial.print("Yaw (");
    Serial.print(trim);
    Serial.print("): ");
    mappedData = map(rawData, 1530, 2000, 0, 255);
    Serial.println(mappedData);
    rawYaw = rawData;
  }

  rawData = pulseIn(pinThrust, HIGH, 25000);
  trim = (rawData < rawThrust) ? '-' : '+';
  if(rawData != rawThrust)
  {
    Serial.print("Thrust (");
    Serial.print(trim);
    Serial.print("): ");
    mappedData = map(rawData, 1530, 2000, 0, 255);
    Serial.println(mappedData);
    rawThrust = rawData;
  }
  
  delay(1000);
}
