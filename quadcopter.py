'''
Quadcopter Main Control Program
Based on: Instructables Driving an ESC Brushless Motor Using Raspberry Pi
http://www.instructables.com/id/Driving-an-ESCBrushless-Motor-Using-Raspberry-Pi/

This program will let you test your ESC and brushless motor.
Make sure your battery is not connected if you are going to calibrate it at first.
'''

# Libraries
import os
import time
import pigpio

os.system ("sudo pigpiod")

# Time delay of 1 second required for RPI
time.sleep(1) 

# Connect GPIO pins to ESCs
propPinBL = 4
propPinBR = 17 # Blue wires
propPinFR = 27 # Red wires
propPinFL = 22 # Green wires

piBL = pigpio.pi();
piBL.set_servo_pulsewidth(propPinBL, 0) 
piBR = pigpio.pi();
piBR.set_servo_pulsewidth(propPinBR, 0) 
piFR = pigpio.pi();
piFR.set_servo_pulsewidth(propPinFR, 0) 
piFL = pigpio.pi();
piFL.set_servo_pulsewidth(propPinFL, 0) 

maxValue = 2000
minValue = 700
startingSpeed = 1500

"""
Function Name: manualDrive
Description: Program your ESC, if required
Parameters: N/A
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
Function Name: calibrate
Description: This is the auto calibration procedure of a normal ESC
Parameters: N/A
Return:N/A
"""                
def calibrate(pi, propPin):
    pi.set_servo_pulsewidth(propPin, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(propPin, maxValue)
        print("Connect the battery. Wait for two beeps and a gradual falling tone, then press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(propPin, minValue)
            print("Sleep for 7...")
            time.sleep(7)
            print("Sleep for 5...")
            time.sleep (5)
            print("Setting servo pulse width...")
            pi.set_servo_pulsewidth(propPin, 0)
            time.sleep(2)
            print("Arming ESC...")
            pi.set_servo_pulsewidth(propPin, minValue)
            time.sleep(1)
            print("Control start...")
            control()

"""
Function Name: control
Description: Control motor
Parameters: N/A
Return: N/A
"""  
def control(pi, propPin): 
    print("Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
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
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manualDrive()
            break
        elif inp == "arm":
            arm()
            break	
        else:
            print("Please press a, q, d OR e")

"""
Function Name: arm
Description: This is the arming procedure of an ESC 
Parameters: N/A
Return: N/A
"""              
def arm(pi, propPin):
    print("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        pi.set_servo_pulsewidth(propPin, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(propPin, maxValue)
        time.sleep(1)
        pi.set_servo_pulsewidth(propPin, minValue)
        time.sleep(1)
        control() 

"""
Function Name: arm
Description: Stop every action your Pi is performing for ESC ofcourse.
Parameters: N/A
Return:N/A
"""           
def stop(pi, propPin):
    pi.set_servo_pulsewidth(propPin, 0)
    pi.stop()

#Start of the program
print("Type bl OR br OR fr OR fl to choose motor")
inp = input()
if inp == "bl":
    pi = piBL
    propPin = propPinBL
elif inp == "br":
    pi = piBR
    propPin = propPinBR
elif inp == "fr":
    pi = piFR
    propPin = propPinFR
elif inp == "fl":
    pi = piFL
    propPin = propPinFL
else :
    print("Type bl OR br OR fr OR fl to choose motor")

print("For first time launch, select calibrate")    
print("Type the exact word for the function you want")
print("calibrate OR manual OR control OR arm OR stop")    
inp = input()
if inp == "manual":
    manualDrive(pi, propPin)
elif inp == "calibrate":
    calibrate(pi, propPin)
elif inp == "arm":
   arm(pi, propPin)
elif inp == "control":
    control(pi, propPin)
elif inp == "stop":
    stop(pi, propPin)
else :
    print("Please reset")