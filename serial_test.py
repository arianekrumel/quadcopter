import serial

ser=serial.Serial("/dev/ttyACM1", 9600);
ser.baudrate=9600;

while 1:
    input = ser.readline();
    print(input.decode("utf-8"))