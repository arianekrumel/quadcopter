/*
 * Flight Controller with Interrupts
 *
 * This is an Arduino application that connects with
 * controller through receiver system
 *
 * The circuit:
 * * Arduino Mega2560
 * * Fly Sky FS-T6 Controller
 * * Fly Sky FS-R6B
 *
 * 5/8/18
 * Ariane Krumel
 *
 *
 * Based on https://www.youtube.com/watch?v=v_N5HmXmDyk
 * and https://www.youtube.com/watch?v=ncBDvcbY1l4
*/

int pinRoll   = 53; // Channel 1
int pinPitch  = 52; // Channel 2
int pinThrust = 51; // Channel 3
int pinYaw    = 50; // Channel 4

double chl[4] = {0, 0, 0, 0};

int mappedData = 0;

void setup() {
  delay(1000);
  pinMode(pinRoll, INPUT);
  pinMode(pinPitch, INPUT);
  pinMode(pinThrust, INPUT);
  pinMode(pinYaw, INPUT);
  Serial.begin(9600);
}

void loop() {
  chl[0] = pulseIn(pinRoll, HIGH, 25000);
  chl[1] = pulseIn(pinPitch, HIGH, 25000);
  chl[2] = pulseIn(pinThrust, HIGH, 25000);
  chl[3] = pulseIn(pinYaw, HIGH, 25000);
  
  Serial.print("Roll: ");
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
}
