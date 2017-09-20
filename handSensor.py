# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Created Daichi Hayashi 2017/09/19
# From Yonago Institute of Technology
# Copyright ©️ 2017 Daichi Hayashi. All rights reserved.

# move 3 fingers following to proximity sensors
# this might be main program

# ========== import ==========
import pigpio
from gpiozero import MCP3208
from time import sleep

adc0 = MCP3208(channel = 0)
adc1 = MCP3208(channel = 1)
adc2 = MCP3208(channel = 2)
pwm = pigpio.pi()

# ========== constants ==========
FING1_PIN    = 15
FING2_PIN    = 18
FING3_PIN    = 23
JOINT_PIN    = 24
# Threshold of Proximity sensor
GET_OBJECT   = 0.8
NEAR_OBJECT  = 0.5
CLOSE_OBJECT = 0.2
TOUCH_OBJECT = 0.1
# speed of servoMotor
MAX_SPEED = 2.0
MID_SPEED = 1.0
MIN_SPEED = 0.5

# ========== variables ==========
command    = 0 # 0:OPEN, 1:CLOSE
stateFing1 = 0 # distance between fing to object
stateFing2 = 0 # state assignments 0:far 1:mid 2:close
stateFing3 = 0 # 0:far 1:mid 2:close

microSec1  = 0.0 # servo usec
microSec2  = 0.0
microSec3  = 0.0
degree1    = 0.0 # servo angle
degree2    = 0.0
degree3    = 0.0

# ========== Function moving servoMotor ==========
def moveServo(pin, degree):
    # servoMotor cannot move over 60[deg] and under -60[deg]
    if degree <= 60.0 and degree >= -60.0:
        usec = 1500.0 + (degree * 10.0)
        pi.set_servo_pulsewidth(pin, usec)
        sleep(0.1)

# ========== Function commanding servoMotor ==========
def cmdServo(adcChannel, degree, state):
    # store in tuple
    adcTuple = (adc0.value, adc1.value, adc2.value)

    # touch to object
    if adcTuple[adcChannel] <= TOUCH_OBJECT:
        # change state and show message in first change
        if state not 3:
            state = 3
            print("Finger" + str(adcChannel + 1) + "has been changed to state1")
    # close to object
    elif adcTuple[adcChannel] <= CLOSE_OBJECT:
        degree -= MIN_SPEED
        # change state and show message in first change
        if state not 2:
            state = 2
            print("Finger" + str(adcChannel + 1) + "has been changed to state1")
    # mid distance to object
    elif adcTuple[adcChannel] <= NEAR_OBJECT:
        degree -= MID_SPEED
        # change state and show message in first change
        if state not 1:
            state = 1
            print("Finger" + str(adcChannel + 1) + "has been changed to state1")
    # far from object
    else:
        degree -= MAX_SPEED
        state = 0

    return degree, state

# ========== initialize ==========
# set to 0[deg] all servoMotor
moveServo(FING1_PIN, 0)
moveServo(FING2_PIN, 0)
moveServo(FING3_PIN, 0)
moveServo(JOINT_PIN, 0)

# ========== main ==========
try:
    # Loop for infinite
    while True:
        # command input
        command = int(input("Type '0':OPEN, '1':CLOSE ...:"))

        # OPEN command
        if command == 0:
            print("opening fingers")
            ''' Need speed control method in this area too '''
            moveServo(FING1_PIN, 0.0)
            moveServo(FING2_PIN, 0.0)
            moveServo(FING3_PIN, 0.0)

        # CLOSE command
        elif command == 1:
            print("closing fingers")
            # until ALL fingers touch to object
            while (stateFing1 not 3) or (stateFing2 not 3) or (stateFing3 not 3):
                # USAGE: cmdServo(channel of ADC, degree, state)
                degree1, stateFing1 = cmdServo(0, degree1, stateFing1)
                degree2, stateFing2 = cmdServo(1, degree2, stateFing2)
                degree3, stateFing3 = cmdServo(2, degree3, stateFing3)
                # move servoMotors according to angle value of cmdServo
                moveServo(FING1_PIN, degree1)
                moveServo(FING2_PIN, degree2)
                moveServo(FING3_PIN, degree3)

        # Typed wrong command
        else:
            print("Error command typed...")

except KeyboardInterrupt:
elif:
    pass

# ========== destroy ==========
# force to stop PWM by handing '0' to second arguement
pi.set_servo_pulsewidth(FING1_PIN, 0)
pi.set_servo_pulsewidth(FING2_PIN, 0)
pi.set_servo_pulsewidth(FING3_PIN, 0)
pi.set_servo_pulsewidth(JOINT_PIN, 0)

# end of program
