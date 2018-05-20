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

// IMU
Adafruit_BNO055 bno = Adafruit_BNO055(55);

int activeIdx = 0;

#define PIN_CHL1_ROLL   53 // Channel 1
#define PIN_CHL2_PITCH  52 // Channel 2
#define PIN_CHL3_THRUST 51 // Channel 3
#define PIN_CHL4_YAW    50 // Channel 4

int commandsDisplay[4] = {0, 0, 0, 0};
const int rollIdx = 0;
const int pitchIdx = 1;
const int thrustIdx = 2;
const int yawIdx = 3;

int actualOrientations[3] = {0, 0, 0};
const int orientationIndexYaw = 0;
const int orientationIndexPitch = 1;
const int orientationIndexRoll = 2;

const int rollMinRx = 1000;
const int rollMaxRx = 2000;
const int rollMinDisplay = -180;
const int rollMaxDisplay = 180;

const int pitchMinRx = 1000;
const int pitchMaxRx = 2000;
const int pitchMinDisplay = -90;
const int pitchMaxDisplay = 90;

const int thrustMinRx = 1000;
const int thrustMaxRx = 2000;
const int thrustMinDisplay = 0;
const int thrustMaxDisplay = 10;

const int yawMinRx = 1000;
const int yawMaxRx = 2000;
const int yawMinDisplay = 0;
const int yawMaxDisplay = 360;

/*
 *Function Name: setup
 *Description: TBD
 *Parameters: N/A
 *Return:N/A
*/
void setup() {
  // Set up pin change interuppts for our
  // RC receiver PWM input
  PCICR |= (1 << PCIE0);
  PCMSK0 |= (1 << PCINT0);
  
  pinMode(PIN_CHL1_ROLL, INPUT);
  pinMode(PIN_CHL2_PITCH, INPUT);
  pinMode(PIN_CHL3_THRUST, INPUT);
  pinMode(PIN_CHL4_YAW, INPUT);
  
  Serial.begin(9600);
  //Serial.println("Flight Control"); 
  //Serial.println("");

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

/*
 *Function Name: loop
 *Description: TBD
 *Parameters: N/A
 *Return:N/A
*/
void loop() {
  // Get PID values
  getPID();
}

/*
 *Function Name: getPID
 *Description: TBD
 *Parameters: N/A
 *Return:N/A
*/
void getPID(){
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Display the orientation data */
  actualOrientations[orientationIndexYaw] = event.orientation.x; 
  actualOrientations[orientationIndexPitch] = event.orientation.y; 
  actualOrientations[orientationIndexRoll] = event.orientation.z; 
  
  Serial.print("yaw:");
  Serial.println(actualOrientations[orientationIndexYaw]);
  delay(100);
  Serial.print("pitch:");
  Serial.println(actualOrientations[orientationIndexPitch]);
  delay(100);
  Serial.print("roll:");
  Serial.println(actualOrientations[orientationIndexRoll]);
  delay(100);
}

/*
 *Function Name: PCINT0_vect
 *Description: Handler for command interrupt
 *Parameters: N/A
 *Return:N/A
*/
ISR(PCINT0_vect){ 
     
  // Round robin check on commanded pins
  if(activeIdx == rollIdx) {
    activeIdx = pitchIdx;
    commandsDisplay[rollIdx] = pulseIn(PIN_CHL1_ROLL, HIGH, 25000);
  } 
  else if(activeIdx == pitchIdx) {
    activeIdx = thrustIdx;
    commandsDisplay[pitchIdx] = pulseIn(PIN_CHL2_PITCH, HIGH, 25000);
  } 
  else if(activeIdx == thrustIdx) {
    activeIdx = yawIdx;
    commandsDisplay[thrustIdx] = pulseIn(PIN_CHL3_THRUST, HIGH, 25000);
  } 
  else if(activeIdx == yawIdx) {
    activeIdx = rollIdx;
    commandsDisplay[yawIdx] = pulseIn(PIN_CHL4_YAW, HIGH, 25000);
  } 

  Serial.print("rollCmd:");
  Serial.println(map(commandsDisplay[rollIdx], rollMinRx, rollMaxRx, rollMinDisplay, rollMaxDisplay));
  delay(100);
  
  Serial.print("pitchCmd:");
  Serial.println(map(commandsDisplay[pitchIdx], pitchMinRx, pitchMaxRx, pitchMinDisplay, pitchMaxDisplay)); 
  delay(100);
    
  Serial.print("thrustCmd:");
  Serial.println(map(commandsDisplay[thrustIdx], thrustMinRx, thrustMaxRx, thrustMinDisplay, thrustMaxDisplay));
  delay(100); 

  Serial.print("yawCmd:");
  Serial.println(map(commandsDisplay[yawIdx], yawMinRx, yawMaxRx, yawMinDisplay, yawMaxDisplay));
  delay(100); 
}

