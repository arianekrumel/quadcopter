/*
   ReadPWM

   This is an Arduino application that connects with
   controller through receiver system

   The circuit:
 * * Arduino Mega2560
 * * Fly Sky FS-T6 Controller
 * * Fly Sky FS-R6B

   5/6/18
   Ariane Krumel


   Based on https://www.youtube.com/watch?v=v_N5HmXmDyk
*/


void setup() {
  delay(1000);
  pinMode(3, INPUT);
  Serial.begin(9600);
}

void loop() {
  int v = pulseIn(3, HIGH, 25000);
  Serial.println(v);
  delay(500);
  //Serial.println("Test");
}



