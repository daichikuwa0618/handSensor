# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Created Daichi Hayashi 2017/12/18
# From Yonago Institute of Technology
# Copyright ©️ 2017 Daichi Hayashi. All rights reserved.

# move 3 fingers following to proximity sensors
# this might be main program
# this program is made for an experiment

# ========== import ==========
import pigpio
from gpiozero import MCP3208
import time
from datetime import datetime

adc0 = MCP3208(channel = 0)

Vref = 5.05 # reference voltage of MCP3208

pwm = pigpio.pi()

# ========== constants ==========
fing0Pin = 15
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
    # round up
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
            # 実験開始日時を書き込む
            f.write("====================\n" + str(datetime.now()) + "\n")
            # 各定数を記載する
            f.write("[stopDst, maxDst, maxSpeed, minSpeed, interval] = " + str(dataList))

        # set to 0[deg] all servoMotor
        moveServo(fing0Pin, 0)
        # Loop for infinite
        while True:
            # command input
            command = int(input("Type '0':OPEN, '1':CLOSE(with sensor), '2':CLOSE(without sensor) ...:"))

            # OPEN command
            if command == 0:
                print("opening fingers")
                # Need speed control method in this area too
                moveServo(fing0Pin, -60.0)
                degree0 = -60.0

            # CLOSE command
            elif command == 1:
                with open("expData.txt", "a") as f:
                    # put index
                    f.write("\n\n========== with sensor ==========\n")
                    f.write("time     deg\n")
                print("closing fingers")
                startTime = time.time()
                # until ALL fingers touch to object
                while VtoD(adc0.value * Vref) >= stopDst:
                    # cal current distance
                    dstValue   = VtoD(adc0.value * Vref)
                    # cal current angular velocty[deg/sec]
                    speedValue = DtoS(dstValue)
                    # need to times interval to correct speed for [deg/sec]
                    degree0 += (speedValue * interval)
                    # move motor
                    moveServo(fing0Pin, degree0)
                    # interval
                    time.sleep(interval)
                    # write to file
                    with open("expData.txt", "a") as f:
                        # write experiment data
                        f.write(str(time.time() - startTime) + " " + str(dstValue) + " " + str(speedValue) + "\n")
                    print ("time:" + str(time.time() - startTime) + ", dst:" + str(dstValue) + ", speed:" + str(speedValue))
                print ("end of closing")

            elif command == 2:
                with open("expData.txt", "a") as f:
                    # put index
                    f.write("\n\n========== withOUT sensor ==========\n")
                    f.write("time     deg\n")
                print("closing without sensor")
                startTime = time.time()
                while VtoD(adc0.value * Vref) >= stopDst:
                    # cal values
                    dstValue = VtoD(adc0.value * Vref)
                    degree0 += maxSpeed * interval
                    moveServo(fing0Pin, degree0)
                    with open("expData.txt", "a") as f:
                        # write experiment data
                        f.write(str(time.time() - startTime) + " " + str(dstValue) + "\n")
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

# end of program
