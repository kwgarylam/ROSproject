'''
pip install RPi.GPIO

-The program is used to test the motor driver.
-The motor driver used is the L298n.
-The base package used is the Rpi GPIO
Ref: https://www.youtube.com/watch?v=0lXY87NwVIc
'''

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

EnaA = 2
In1A = 3
In1B = 4

EnaB = 17
In2A = 22
In2B = 27

GPIO.setup(EnaA, GPIO.OUT)
GPIO.setup(In1A, GPIO.OUT)
GPIO.setup(In1B, GPIO.OUT)
pwmA = GPIO.PWM(EnaA, 100)
pwmA.start(0)

GPIO.setup(EnaB, GPIO.OUT)
GPIO.setup(In2A, GPIO.OUT)
GPIO.setup(In2B, GPIO.OUT)
pwmB = GPIO.PWM(EnaB, 100)
pwmB.start(0)


###
pwmA.ChangeDutyCycle(60)
GPIO.output(In1A, GPIO.LOW)
GPIO.output(In1B, GPIO.HIGH)

pwmB.ChangeDutyCycle(60)
GPIO.output(In2A, GPIO.LOW)
GPIO.output(In2B, GPIO.HIGH)

sleep(2)
pwmA.ChangeDutyCycle(0)
pwmB.ChangeDutyCycle(0)
