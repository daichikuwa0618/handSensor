# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Created Daichi Hayashi 2017/10/04
# From Yonago Institute of Technology
# Copyright ©️ 2017 Daichi Hayashi. All rights reserved.


# One finger ver. of "handSendor.py" in same directory

# ========== import ==========
import pigpio
from gpiozero import MCP3208
import time

adc0 = MCP3208(channel = 0)

pwm = pigpio.pi()

# ========== constants ==========
fing0Pin    = 15
# Threshold of Proximity sensor
GET_OBJECT   = 0.7
NEAR_OBJECT  = 0.5
CLOSE_OBJECT = 0.2
TOUCH_OBJECT = 0.05
# speed of servoMotor[deg]
MAX_DEG = 2.0
MID_DEG = 1.0
MIN_DEG = 0.5

# ========== variables ==========
command    = 0 # 0:OPEN, 1:CLOSE
stateFing0 = 0 # distance between fing to object
degree0    = 0.0 # servo angle for each servoMotors

# ========== Function moving servoMotor ==========
def moveServo(pin, degree):
    # servoMotor cannot move over 60[deg] and under -60[deg]
    if degree <= 60.0 and degree >= -60.0:
        usec = 1500.0 + (degree * 10.0)
        pwm.set_servo_pulsewidth(pin, usec)
        # print(str(degree) + "deg" + str(usec) + "usec")

# ========== Function commanding servoMotor ==========
def cmdServo(adcChannel, degree, state):
    # store in tuple
    adcList = [adc0.value]

    adcList[adcChannel] = float(input("value:"))

    # touch to object
    if adcList[adcChannel] <= TOUCH_OBJECT:
        # change state and show message in first change
        if state != 3:
            state = 3
            print("Finger" + str(adcChannel) + "has been changed to state3")
    # close to object
    elif adcList[adcChannel] <= CLOSE_OBJECT:
        degree -= MIN_DEG
        # change state and show message in first change
        if state != 2:
            state = 2
            print("Finger" + str(adcChannel) + "has been changed to state2")
    # mid distance to object
    elif adcList[adcChannel] <= NEAR_OBJECT:
        degree -= MID_DEG
        # change state and show message in first change
        if state != 1:
            state = 1
            print("Finger" + str(adcChannel) + "has been changed to state1")
    # far from object
    else:
        degree -= MAX_DEG
        state = 0

    return degree, state


# ========== main ==========
if __name__ == '__main__':
    try:
        # set to 0[deg] all servoMotor
        moveServo(fing0Pin, 0.0)
        # Loop for infinite
        while True:
            # command input
            command = int(input("Type '0':OPEN, '1':CLOSE ...:"))

            # OPEN command
            if command == 0:
                print("opening fingers")
                # Need speed control method in this area too
                moveServo(fing0Pin, 0.0)

            # CLOSE command
            elif command == 1:
                print("closing fingers")
                # until ALL fingers touch to object
                while stateFing0 != 3:
                    # USAGE: cmdServo(channel of ADC, degree, state)
                    degree0, stateFing0 = cmdServo(0, degree0, stateFing0)
                    # move servoMotors according to angle value of cmdServo
                    moveServo(fing0Pin, degree0)
                    time.sleep(0.1)

            # Typed wrong command
            else:
                print("Error command typed...")

    except KeyboardInterrupt:
        pass

# ========== destroy ==========
# force to stop PWM by handing '0' to second arguement
pwm.set_servo_pulsewidth(fing0Pin, 0)

# end of program