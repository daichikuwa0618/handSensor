# -*- coding: utf-8 -*-
#!/usr/bin/env python

# move 3 fingers following to proximity sensors
# this might be main program

# ========== import ==========
import pigpio
from gpiozero import MCP3208
from time import sleep

adc = MCP3208(channel = 0)
pwm = pigpio.pi()

# ========== 定数 ==========
FING1_PIN    = 15
FING2_PIN    = 18
FING3_PIN    = 23
JOINT_PIN    = 24
# 近接センサの閾値
GET_OBJECT   = 0.8
NEAR_OBJECT  = 0.3
TOUCH_OBJECT = 0.1

# ========== 変数 ==========
command   = 0 # 0:OPEN, 1:CLOSE
state     = 0 # distance between fing to object
microSec1 = 0.0 # servo usec
microSec2 = 0.0
microSec3 = 0.0
degree1   = 0.0 # servo angle
degree2   = 0.0
degree3   = 0.0

# ========== Function moving servoMotor ==========
def moveServo(pin, degree):
    usec = 1500.0 + (degree * 10.0)
    pi.set_servo_pulsewidth(pin, usec)

# ========== initialize ==========
# set to 0[deg] all servoMotor
moveServo(FING1_PIN, 0)
moveServo(FING2_PIN, 0)
moveServo(FING3_PIN, 0)
moveServo(JOINT_PIN, 0)

# ========== main ==========
try:
except KeyboardInterrupt:
    pass

# ========== destroy ==========
# force to stop PWM by handing '0' to second arguement
pi.set_servo_pulsewidth(FING1_PIN, 0)
pi.set_servo_pulsewidth(FING2_PIN, 0)
pi.set_servo_pulsewidth(FING3_PIN, 0)
pi.set_servo_pulsewidth(JOINT_PIN, 0)

# end of program
