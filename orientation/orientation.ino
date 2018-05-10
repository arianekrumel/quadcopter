/*
 * orientation
 *
 * This is an Arduino application that receives
 * three dimensions of orientation
 *
 * The circuit:
 * * Arduino Mega2560
 * * Adafruit BNO005
 *
 * 5/8/18
 * Ariane Krumel
 * 
 * 
 * Based on https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup(void)
{
  delay(1000);
  Serial.begin(9600);
  Serial.println("Orientation Sensor Test"); Serial.println("");

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

void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Display the floating point data */
  Serial.print("Yaw: ");
  Serial.print(event.orientation.x, 4);
  Serial.print("\tPitch: ");
  Serial.print(event.orientation.y, 4);
  Serial.print("\tRoll: ");
  Serial.print(event.orientation.z, 4);
  Serial.println("");

  delay(100);
}
