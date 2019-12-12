import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)

TRIG1 = 24
ECHO1 = 12

#print ("Distance Measurement In Process")
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.output(TRIG1, False)

GPIO.setup(ECHO1, GPIO.IN)

#print ("Waiting For Sensor1 To Settle") 
time.sleep(.1)
GPIO.output(TRIG1, True)
time.sleep(0.00001)
GPIO.output(TRIG1, False)

while GPIO.input(ECHO1) == 0:
    pass
    pulse_start1 = time.time()
 
while GPIO.input(ECHO1) == 1:
    pass
    pulse_end1 = time.time()

pulse_duration1 = pulse_end1 - pulse_start1

distance1 = pulse_duration1 * 17150
distance1= round(distance1, 2)
print ("Distance1:",distance1, "cm")

time.sleep(10)

GPIO.cleanup()