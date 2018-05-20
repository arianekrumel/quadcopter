'''
Quadcopter Main Control Program
Based on: Instructables Driving an ESC Brushless Motor Using Raspberry Pi
http://www.instructables.com/id/Driving-an-ESCBrushless-Motor-Using-Raspberry-Pi/
'''

# Libraries
import os
import time
import pigpio
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

os.system ("sudo pigpiod")

# Time delay of 1 second required for RPI
time.sleep(1) 

# Connect GPIO pins to ESCs
propPins = {'bl':4, 'br':17, 'fr':27, 'fl':22}
propPins['bl'] = 4
propPins['br'] = 17 # Blue wires
propPins['fr'] = 27 # Red wires
propPins['fl'] = 22 # Green wires

piBL = pigpio.pi();
piBL.set_servo_pulsewidth(propPins['bl'], 0) 
piBR = pigpio.pi();
piBR.set_servo_pulsewidth(propPins['br'], 0) 
piFR = pigpio.pi();
piFR.set_servo_pulsewidth(propPins['fr'], 0) 
piFL = pigpio.pi();
piFL.set_servo_pulsewidth(propPins['fl'], 0) 

maxValue = 2000
minValue = 700
startingSpeed = 700

"""
Function Name: arm
Description: Stop every action your Pi is performing for ESC of course.
Parameters: N/A
Return:N/A
"""           
def stop(pi, propPin):
    pi.set_servo_pulsewidth(propPin, 0)
    pi.stop(pi, propPin)

"""
Function Name: manualDrive
Description: Program your ESC, if required
Parameters: N/Api.set_servo_pulsewidth(propPin,inp)
Return:N/A
"""
def manualDrive(pi, propPin):
    print("You have selected manual option so give a value between 0 and you max value")   
    while True:
        inp = input()
        if inp == "stop":
            stop(pi, propPin)
            break
        elif inp == "control":
            control(pi, propPin)
            break
        elif inp == "arm":
            arm(pi, propPin)
            break	
        else:
            pi.set_servo_pulsewidth(propPin,inp)

"""
Function Name: calibrateAll
Description: This is the auto calibration procedure of a normal ESC
Parameters: N/A
Return:N/A
""" 
def calibrateAll():
    piBL.set_servo_pulsewidth(propPins['bl'], 0)
    piBR.set_servo_pulsewidth(propPins['br'], 0)
    piFR.set_servo_pulsewidth(propPins['fr'], 0)
    piFL.set_servo_pulsewidth(propPins['fl'], 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        piBL.set_servo_pulsewidth(propPins['bl'], maxValue)
        piBR.set_servo_pulsewidth(propPins['br'], maxValue)
        piFR.set_servo_pulsewidth(propPins['fr'], maxValue)
        piFL.set_servo_pulsewidth(propPins['fl'], maxValue)
        print("Connect the battery. Wait for two beeps and a gradual falling tone, then press Enter")
        inp = input()
        if inp == '':            
            piBL.set_servo_pulsewidth(propPins['bl'], minValue)
            piBR.set_servo_pulsewidth(propPins['br'], minValue)
            piFR.set_servo_pulsewidth(propPins['fr'], minValue)
            piFL.set_servo_pulsewidth(propPins['fl'], minValue)
            print("Sleep for 7...")
            time.sleep(7)
            print("Sleep for 5...")
            time.sleep (5)
            print("Setting servo pulse width...")
            piBL.set_servo_pulsewidth(propPins['bl'], 0)
            piBR.set_servo_pulsewidth(propPins['br'], 0)
            piFR.set_servo_pulsewidth(propPins['fr'], 0)
            piFL.set_servo_pulsewidth(propPins['fl'], 0)
            time.sleep(2)
            print("Arming ESC...")
            piBL.set_servo_pulsewidth(propPins['bl'], minValue)
            piBR.set_servo_pulsewidth(propPins['br'], minValue)
            piFR.set_servo_pulsewidth(propPins['fr'], minValue)
            piFL.set_servo_pulsewidth(propPins['fl'], minValue)
            time.sleep(1)
            print("Calibrated and armed...")

"""
Function Name: thrustAll
Description: TBD
Parameters: N/A
Return: N/A
"""  
def thrustAll(speed):
    piBL.set_servo_pulsewidth(propPins['bl'], speed)
    piBR.set_servo_pulsewidth(propPins['br'], speed)
    piFR.set_servo_pulsewidth(propPins['fr'], speed)
    piFL.set_servo_pulsewidth(propPins['fl'], speed)

"""
Function Name: control
Description: Control motor
Parameters: N/A
Return: N/A
"""  
def control(pi, propPin): 
    print("Starting the motor, I hope its calibrated and armed, if not restart prompt by giving 'x'")
    time.sleep(1)
    
    speed = startingSpeed
    print("Controls - a: decrease speed & d: increase speed OR q: decrease a lot of speed & e: increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(propPin, speed)
        inp = input()
        
        if inp == "q":
            speed -= 100    # decrementing the speed like hell
            print("speed = {}".format(speed))
        elif inp == "e":    
            speed += 100    # incrementing the speed like hell
            print("speed = {}".format(speed))
        elif inp == "d":
            speed += 10     # incrementing the speed 
            print("speed = {}".format(speed))
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print("speed = {}".format(speed))
        elif inp == "stop":
            stop(pi, propPin)          #going for the stop function
            break
        elif inp == "manual":
            manualDrive(pi, propPin)
            break
        elif inp == "arm":
            arm(pi, propPin)
            break	
        else:
            print("Please press a, q, d OR e")

"""
Function Name: mainprint("speed = {}".format(speed))
Description: TBD 
Parameters: N/A
Return: N/A
"""  
def main():
    #print("Calibrate all for first time launch")
    #calibrateAll()
    
    print(ser.name)
    ser.write(b'hello')
    
    # Establish serial connection with controller
    thrustCurrent = 0
    thrustInput = 0
    
    while 1 :
    	str = "thrust:0"#ser.readline()
    	strArr = str.split(':')
    	if(strArr[0] == 'thrust'):
            thrustInput = int(strArr[1])
            
            if(thrustInput > thrustCurrent):
                thrustAll(thrustInput)
            if(thrustInput < thrustCurrent):
                thrustAll(thrustInput)
                
            thrustCurrent = thrustInput
            print("speed = {}".format(thrustCurrent))
            
        #if(strArr[0] = 'stop'):
            #break
    	
      
    #while True:
        #inp = input()
        #if inp == "manual":
            #manualDrive(pi, propPin)
  	    #elif inp == "control":
  	        #control(pi, propPin)
  	    #elif inp == "stop":
 	        #stop(pi, propPin)

#Start of the program
if __name__ == '__main__':
	main()