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
propPins = {
	'bl':4, 
	'br':17, # Blue wires
	'fr':27, # Red wires
	'fl':22 # Green wires
}

piBL = pigpio.pi();
piBL.set_servo_pulsewidth(propPins['bl'], 0) 
piBR = pigpio.pi();
piBR.set_servo_pulsewidth(propPins['br'], 0) 
piFR = pigpio.pi();
piFR.set_servo_pulsewidth(propPins['fr'], 0) 
piFL = pigpio.pi();
piFL.set_servo_pulsewidth(propPins['fl'], 0) 

maxValue = 1800
minValue = 700
startingSpeed = 800
speedCurrent = {'bl':startingSpeed, 'br':startingSpeed, 'fr':startingSpeed, 'fl':startingSpeed}

"""
Function Name: stopAll
Description: Stop every action your Pi is performing for ESC of course.
Parameters: N/A
Return:N/A
"""           
def stopAll():
    piBL.set_servo_pulsewidth(propPins['bl'], 0)
    piBR.set_servo_pulsewidth(propPins['br'], 0)
    piFR.set_servo_pulsewidth(propPins['fr'], 0)
    piFL.set_servo_pulsewidth(propPins['fl'], 0)
    
    
    piBL.stop(piBL, propPins['bl'])
    piBR.stop(piBR, propPins['br'])
    piFR.stop(piFR, propPins['fr'])
    piFL.stop(piFL, propPins['fl'])

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
Function Name: setSpeed
Description: TBD
Parameters: N/A
Return: N/A
"""  
def setSpeed():
    if(speedCurrent['bl'] > maxValue):
        speedCurrent['bl'] = maxValue
    if(speedCurrent['bl'] < minValue):
        speedCurrent['bl'] = minValue
    piBL.set_servo_pulsewidth(propPins['bl'], speedCurrent['bl'])
    
    if(speedCurrent['br'] > maxValue):
        speedCurrent['br'] = maxValue
    if(speedCurrent['br'] < minValue):
        speedCurrent['br'] = minValue
    piBR.set_servo_pulsewidth(propPins['br'], speedCurrent['br'])
    
    if(speedCurrent['fr'] > maxValue):
        speedCurrent['fr'] = maxValue
    if(speedCurrent['fr'] < minValue):
        speedCurrent['fr'] = minValue
    piFR.set_servo_pulsewidth(propPins['fr'], speedCurrent['fr'])
    
    if(speedCurrent['fl'] > maxValue):
        speedCurrent['fl'] = maxValue
    if(speedCurrent['fl'] < minValue):
        speedCurrent['fl'] = minValue
    piFL.set_servo_pulsewidth(propPins['fl'], speedCurrent['fl'])
    
    print("Set speed")

"""
Function Name: thrustPID
Description: TBD
Parameters: N/A
Return: N/A
"""  
def thrustPID(inp):
    speedCurrent['bl'] = inp
    speedCurrent['br'] = inp
    speedCurrent['fr'] = inp
    speedCurrent['fl'] = inp
    #if(thrustCommanded > inp): # decrementing the speed 
    	#speedCurrent['bl'] -= 100
    	#speedCurrent['br'] -= 100
    	#speedCurrent['fr'] -= 100
    	#speedCurrent['fl'] -= 100
    #if(thrustCommanded < inp): # incrementing the speed
    	#speedCurrent['bl'] += 100
    	#speedCurrent['br'] += 100
    	#speedCurrent['fr'] += 100
    	#speedCurrent['fl'] += 100
    thrustCommanded = inp
    
    setSpeed()

"""
Function Name: rollPID
Description: TBD
Parameters: N/A
Return: N/A
"""  
def rollPID(rollCommanded, rollMeasured):
    if(rollCommanded > rollMeasured): # thrust on left 2 blades is higher than right 2 
        print("Roll: thrust on left 2 blades is higher than right 2")
        speedCurrent['bl'] -= 50 # lower left 2
        speedCurrent['br'] += 50 # boost right 2
        speedCurrent['fr'] += 50
        speedCurrent['fl'] -= 50
        setSpeed()
    if(rollCommanded < rollMeasured): # thrust on right 2 blades is higher than left 2
        print("Roll: thrust on right 2 blades is higher than left 2")
        speedCurrent['bl'] += 50 # boost left 2
        speedCurrent['br'] -= 50 # lower right 2
        speedCurrent['fr'] -= 50
        speedCurrent['fl'] += 50
        setSpeed()
    
    return rollMeasured

"""
Function Name: pitchPID
Description: TBD
Parameters: N/A
Return: N/A
"""  
def pitchPID(pitchCommanded, pitchMeasured):
    if(pitchCommanded > pitchMeasured): # thrust on back 2 blades is higher than front 2
        print("Pitch: thrust on back 2 blades is higher than front 2")
        speedCurrent['bl'] -= 50 # lower back 2
        speedCurrent['br'] -= 50
        speedCurrent['fr'] += 50 # boost front 2
        speedCurrent['fl'] += 50
        setSpeed()
    if(pitchCommanded < pitchMeasured): # thrust on front 2 blades is higher than back 2
        print("Pitch: thrust on front 2 blades is higher than back 2")
        speedCurrent['bl'] += 50 # boost back 2
        speedCurrent['br'] += 50
        speedCurrent['fr'] -= 50 # lower front 2
        speedCurrent['fl'] -= 50
        setSpeed()
    
    return pitchMeasured

"""
Function Name: yawPID
Description: TBD
Parameters: N/A
Return: N/A
"""  
def yawPID(yawCommanded, yawMeasured):
    if(yawCommanded > yawMeasured): # thrust on 2 CC blades is higher than 2 C 
        print("Yaw: thrust on 2 CC blades is higher than 2 C")
        speedCurrent['bl'] += 50 # boost 2 C
        speedCurrent['br'] -= 50 # lower 2 CC
        speedCurrent['fr'] += 50
        speedCurrent['fl'] -= 50
        setSpeed()
    if(yawCommanded < yawMeasured): # thrust on 2 C blades is higher than 2 CC
        print("Yaw: thrust on 2 C blades is higher than 2 CC")
        speedCurrent['bl'] -= 50 # lower 2 C
        speedCurrent['br'] += 50 # boost 2 CC
        speedCurrent['fr'] -= 50
        speedCurrent['fl'] += 50
        setSpeed()
	
    return yawMeasured

"""
Function Name: main
Description: TBD 
Parameters: N/A
Return: N/A
"""  
def main():
    print("Calibrate all for first time launch")
    calibrateAll()
    
    print("Start motors")
    thrustPID(1000)
    
    thrustCommanded = 0
    rollCommanded = 0
    pitchCommanded = 0
    yawCommanded = 0
    
    print("Establish serial connection with controller")
    
    while True:
    	inp = ser.readline()
    	str = inp.decode('utf-8')
    	strArr = str.split(':')
    	cmd = strArr[0]
    	if(len(strArr) > 1):
            val = int(strArr[1])
    	if(cmd=='roll'):
            rollCommanded = rollPID(rollCommanded, val)
    	elif(cmd == 'pitch'):
            pitchCommanded = pitchPID(pitchCommanded, val)
    	elif(cmd == 'yaw'):
            yawCommanded = yawPID(yawCommanded, val)
    	elif(cmd == 'stop'):
 	    stopAll()

print("Start of the program")
if __name__ == '__main__':
	main()