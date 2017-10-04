#!/usr/bin/env python
# -*- coding: utf-8 -*-

#サーボモータの速度を制御するプログラム
#サーボモータの情報
#周期20msで動作
#1500μsで0deg , 2400μsで+90deg , 600μsで-90deg
#したがって'1deg'動かすのに10μsec変更すれば良い

import pigpio
import time
from time import sleep

pi = pigpio.pi()

#==========ピン番号==========#
SERVO_PIN       = 15

#==========変数宣言==========#
#角度(degree)
latest_degree     = 0 #前回の角度
degree            = 0 #現在の角度
loadstar_degree   = 0 #目標の角度
sec               = 0.1 #停止時間

#パルス幅(*10^-6 sec)
pulse_width       = 1500

pi.set_servo_pulsewidth(SERVO_PIN, 1500)

try:
    while True:
        latest_degree   = loadstar_degree
        degree          = latest_degree
        loadstar_degree = input('角度を入力:')
        sec             = input('動作速度を入力[sec]:')

        loadstar_degree = int(loadstar_degree)
        sec             = float(sec)

        if (loadstar_degree > 60 or loadstar_degree < -60):
            print('60[deg]から-60[deg]で入力してください')
        elif sec > 1:
            print('遅すぎます')
        else:
            #速度変数にあった角度調整
            while degree != loadstar_degree:
                #目標パルスの方が大きい時
                if loadstar_degree - latest_degree >= 0:
                    degree += 1
                else:
                    degree -= 1

                    pulse_width = 1500 - (degree * 10)
                print(str(degree) + ',' + str(pulse_width))
                pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

                time.sleep(sec)
except KeyboardInterrupt: #input CTRL+C
    pass
pi.set_servo_pulsewidth(SERVO_PIN, 0)
