# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Created Daichi Hayashi
# Yonago Institute of Technology
# Copyright ©️ 2017 Daichi Hayashi. All rights reserved.

# move 3 fingers following to proximity sensors

# ========== import ==========
import pigpio
from gpiozero import MCP3208
import time
from datetime import datetime

adc0 = MCP3208(channel = 0)
adc1 = MCP3208(channel = 1)
adc2 = MCP3208(channel = 2)

Vref = 5.05 # reference voltage of MCP3208

pwm = pigpio.pi()

# ========== constants ==========
fing0Pin = 15
fing1Pin = 18
fing2Pin = 23
# Threshold distance to stop motor[mm]
stopDst  = 20.0
# start distance of control[mm]
maxDst   = 100.0
# speed of servoMotor[deg/sec]
maxSpeed = 20.0
# lowest speed
minSpeed = 2.0

# period
interval = 0.05

# this list is for print constants
dataList = [stopDst, maxDst, maxSpeed, minSpeed, interval]

# ========== variables ==========
command = 0 # 0:OPEN, 1:CLOSE
degree0 = 0.0 # servo angle for each servoMotors
degree1 = 0.0
degree2 = 0.0

# ========== trance from Voltage[V] to Distance[mm] ==========
def VtoD(x):
    # y = 1.0006x^5 - 10.824x^4 + 44.431x^3 - 83.573x^2 + 73.991x - 8.9849
    d = (1.0006 * x**5) - (10.824 * x**4) + (44.431 * x**3) - (83.573 * x**2) + (73.991 * x) - 8.9849
    return d # [mm]

# ========== trance from distance[mm] to speed[deg/sec] ==========
def DtoS(x):
    if x > maxDst:
        x = maxDst
    a = (maxSpeed - minSpeed) / (maxDst - stopDst)
    b = maxSpeed - (a * maxDst)
    s = (a * x) + b
    # round down
    if s < minSpeed:
        s = minSpeed
    return s # [deg/sec]

# ========== Function moving servoMotor ==========
def moveServo(pin, degree):
    # servoMotor cannot move over 60[deg] and under -60[deg]
    if degree <= 60.0 and degree >= -60.0:
        usec = 1500.0 + (degree * 10.0)
        pwm.set_servo_pulsewidth(pin, usec)

# ========== main ==========
if __name__ == '__main__':
    try:
        with open("expData.txt", "a") as f:
            # put Experiment date
            f.write("====================\n" + str(datetime.now()) + "\n")
            # write each constants
            f.write("[stopDst, maxDst, maxSpeed, minSpeed, interval] = " + str(dataList))

        # set to 0[deg] all servoMotor
        moveServo(fing0Pin, 0)
        moveServo(fing1Pin, 0)
        moveServo(fing2Pin, 0)
        # Loop infinite
        while True:
            # command input
            command = int(input("Type '0':OPEN, '1':CLOSE(with sensor), '2':CLOSE(without sensor) ...:"))

            # OPEN command
            if command == 0:
                print("opening fingers")
                # Need speed control method in this area too
                moveServo(fing0Pin, 0.0)
                moveServo(fing1Pin, 0.0)
                moveServo(fing2Pin, 0.0)
                degree0 = 0.0
                degree1 = 0.0
                degree2 = 0.0

            # CLOSE command
            elif command == 1:
                with open("expData.txt", "a") as f:
                    # put index
                    f.write("\n\n========== with sensor ==========\n")
                    f.write("time d0 d1 d2 s0 s1 s2 s3\n")
                print("closing fingers")
                startTime = time.time()
                # until ALL fingers touch to object
                while VtoD(adc0.value * Vref) >= stopDst or VtoD(adc1.value * Vref) >= stopDst or VtoD(adc2.value * Vref) >= stopDst:
                    # Calculate current distance [mm]
                    dstValue0   = VtoD(adc0.value * Vref)
                    dstValue1   = VtoD(adc1.value * Vref)
                    dstValue2   = VtoD(adc2.value * Vref)
                    # Calculate current angular velocty [deg/sec]
                    speedValue0 = DtoS(dstValue0)
                    speedValue1 = DtoS(dstValue1)
                    speedValue2 = DtoS(dstValue2)
                    # you need to times the interval to correct speed for [deg/sec]
                    if VtoD(adc0.value * Vref) >= stopDst:
                        degree0 += (speedValue0 * interval)
                    if VtoD(adc1.value * Vref) >= stopDst:
                        degree1 += (speedValue1 * interval)
                    if VtoD(adc2.value * Vref) >= stopDst
                        degree2 += (speedValue2 * interval)
                    # move motors
                    moveServo(fing0Pin, degree0)
                    moveServo(fing1Pin, degree1)
                    moveServo(fing2Pin, degree2)
                    # interval
                    time.sleep(interval)
                    # write to file
                    with open("expData.txt", "a") as f:
                        # write experiment data
                        f.write(str(time.time() - startTime) + " " + str(dstValue0) + " " + str(dstValue1) + " " + str(dstValue2)
                         + " " + str(speedValue0) + " " + str(speedValue1) + " " + str(speedValue2) + "\n")
                    print ("time:" + str(time.time() - startTime) + ", dst0:" + str(dstValue0) + ", speed0:" + str(speedValue0) + ", dst1:" + str(dstValue1) + ", speed1:" + str(speedValue1) + ", dst2:" + str(dstValue2) + ", speed2:" + str(speedValue2))
                print ("end of closing")

            elif command == 2:
                with open("expData.txt", "a") as f:
                    # put index
                    f.write("\n\n========== withOUT sensor ==========\n")
                    f.write("time d0 d1 d2\n")
                print("closing without sensor")
                startTime = time.time()
                while VtoD(adc0.value * Vref) >= stopDst or VtoD(adc1.value * Vref) >= stopDst or VtoD(adc2.value * Vref) >= stopDst:
                    # Calculate Distance
                    dstValue0 = VtoD(adc0.value * Vref)
                    dstValue1 = VtoD(adc1.value * Vref)
                    dstValue2 = VtoD(adc2.value * Vref)
                    if VtoD(adc0.value * Vref) >= stopDst:
                        degree0 += maxSpeed * interval
                    if VtoD(adc1.value * Vref) >= stopDst:
                        degree1 += maxSpeed * interval
                    if VtoD(adc2.value * Vref) >= stopDst:
                        degree2 += maxSpeed * interval
                    moveServo(fing0Pin, degree0)
                    moveServo(fing1Pin, degree1)
                    moveServo(fing2Pin, degree2)
                    with open("expData.txt", "a") as f:
                        # write experiment data
                        f.write(str(time.time() - startTime) + " " + str(dstValue0) + " " + str(dstValue1) + " " + str(dstValue2) + "\n")
                    # interval
                    time.sleep(interval)
                print ("end of closing")

            # Typed wrong command
            else:
                print("Error command typed...")

    except KeyboardInterrupt:
        pass
        # ========== destroy ==========
        # force to stop PWM by handing '0' to second arguement
        pwm.set_servo_pulsewidth(fing0Pin, 0)
        pwm.set_servo_pulsewidth(fing1Pin, 0)
        pwm.set_servo_pulsewidth(fing2Pin, 0)