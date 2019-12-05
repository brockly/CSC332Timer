import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

GPIO.setup(26,GPIO.OUT) #Servo slot 0
GPIO.setup(6,GPIO.OUT)  #Servo slot 1
GPIO.setup(13,GPIO.OUT) #Servo slot 2
GPIO.setup(5,GPIO.OUT)  #Servo slot 3

print("LED on")
GPIO.output(26,GPIO.HIGH)
GPIO.output(6,GPIO.HIGH)
GPIO.output(13,GPIO.HIGH)
GPIO.output(5,GPIO.HIGH)
time.sleep(3)
print("LED off")
GPIO.output(26,GPIO.LOW)
GPIO.output(6,GPIO.LOW)
GPIO.output(13,GPIO.LOW)
GPIO.output(5,GPIO.LOW)