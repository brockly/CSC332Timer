import time
import RPi.GPIO as GPIO

def measure():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
    
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
        
    elapsed = stop-start
    distance = (elapsed * 34300)/2
    
    return distance

def measure_average():
    distance1 = measure()
    time.sleep(0.1)
    distance2 = measure()
    time.sleep(0.1)
    distance3=measure()
    distance = distance1 + distance2 + distance3
    distance = distance/3
    return distance

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 12
GPIO_ECHO = 5

print('Ultrasonic Measurement')

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)

try:
    while True:
        distance = measure_average()
        distanceInches = str(round(distance*0.39, 2))
        print("Distance : %.1f cm" % distance)
        print(distanceInches + " inches")
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()