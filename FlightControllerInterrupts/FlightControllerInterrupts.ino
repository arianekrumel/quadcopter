/*
 * Flight Controller with Interrupts and Orientation
 *
 * This is an Arduino application that connects with
 * controller through receiver system and receives
 * three dimensions of orientation
 *
 * The circuit:
 * * Arduino Mega2560
 * * Fly Sky FS-T6 Controller
 * * Fly Sky FS-R6B
 * * Arduino Mega2560
 * * Adafruit BNO005
 *
 * 5/8/18
 * Ariane Krumel
 *
 *
 * Based on https://www.youtube.com/watch?v=v_N5HmXmDyk
 * and https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
 * and https://www.youtube.com/watch?v=ncBDvcbY1l4
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);

#define PIN_CHL1_ROLL   53 // Channel 1
#define PIN_CHL2_PITCH  52 // Channel 2
#define PIN_CHL3_THRUST 51 // Channel 3
#define PIN_CHL4_YAW    50 // Channel 4

double chl[4] = {0, 0, 0, 0};

int mappedData = 0;

void setup() {
  delay(1000);
  pinMode(PIN_CHL1_ROLL, INPUT);
  pinMode(PIN_CHL2_PITCH, INPUT);
  pinMode(PIN_CHL3_THRUST, INPUT);
  pinMode(PIN_CHL4_YAW, INPUT);
  Serial.begin(9600);
  Serial.println("Flight Control"); 
  Serial.println("");

  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* BNO055 not detected */
    Serial.print("BNO055 not detected, please check your wiring or I2C ADDR.");
    while (1);
  }

  delay(1000);

  bno.setExtCrystalUse(true);
}

void loop() {
  chl[0] = pulseIn(PIN_CHL1_ROLL, HIGH, 25000);
  chl[1] = pulseIn(PIN_CHL2_PITCH, HIGH, 25000);
  chl[2] = pulseIn(PIN_CHL3_THRUST, HIGH, 25000);
  chl[3] = pulseIn(PIN_CHL4_YAW, HIGH, 25000);
  
  Serial.print("COMMANDS");
  
  Serial.print("\tRoll: ");
  mappedData = map(chl[0], 1530, 2000, 0, 255);
  Serial.print(mappedData);

  Serial.print("\tPitch: ");
  mappedData = map(chl[1], 1530, 2000, 0, 255);
  Serial.print(mappedData);

  Serial.print("\tYaw: ");
  mappedData = map(chl[2], 1530, 2000, 0, 255);
  Serial.print(mappedData);
    
  Serial.print("\tThrust: ");
  mappedData = map(chl[3], 1530, 2000, 0, 255);
  Serial.println(mappedData);

  delay(1000);
  
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Display the floating point data */
  Serial.print("ACTUAL");
  
  Serial.print("\tYaw: ");
  Serial.print(event.orientation.x, 4);
  Serial.print("\tPitch: ");
  Serial.print(event.orientation.y, 4);
  Serial.print("\tRoll: ");
  Serial.print(event.orientation.z, 4);
  Serial.println("");
  Serial.println("");
}
