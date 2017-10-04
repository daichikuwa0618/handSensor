#!/usr/bin/env python
# -*- coding: utf-8 -*-

#サーボモータの処理方式によって処理時間がどれだけ変化するのかの検証用プログラム

import pigpio
import time
from time import sleep

pi = pigpio.pi()

#==========定数==========#
SERVO_PIN = 15
FST       = 0.5

#==========変数宣言==========#
#処理時間計測用
start       = 0.0
end         = 0.0
msec        = 0.0
#開閉の判別
state       = 0 #0:周波数 1:角度
#角度(degree)
pre_deg     = 0.0 #前回の角度
degree      = 0.0 #現在の角度
fst_goal    = 0.0 #第1目標の角度(first)
snd_goal    = 0.0 #第2目標(second)
goal_deg    = 0.0 #最終目標角度
#周期(period)
mid_speed   = 0.0 #1番目の周期時間
slow_speed  = 0.0 #2番目の周期時間
#パルス幅(*10^-6 sec)
pulse_width = 900.0 #1500:0deg 2100:60deg 900:-60deg(ccw:正)

#0degに設定
pi.set_servo_pulsewidth(SERVO_PIN, 900)
try:
    while True:
        pre_deg = -60
        degree = pre_deg

        goal_deg = float(input('目標角度を入力してください(-60deg to 60deg)'))
        state    = int(input('周波数:0 角度:1 テスト動作:2 いずれかを入力:'))

        #テスト動作
        if state == 2:
            pulse_width = 1500.0 + (goal_deg * 10.0)
            pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
            #通常動作
            #周波数制御
        elif state == 0:
            print('state = 0:周波数による制御です')
            #実験用
            mid_speed  = float(input('mid_speed :'))
            slow_speed = float(input('slow_speed:'))

            fst_goal = pre_deg + ((goal_deg - pre_deg) * FST)

            if (goal_deg > 60 or goal_deg < -60):
                print('60[deg]から-60[deg]で入力してください')
            else:
                start = time.time()
                #速度変数にあった角度調整
                while degree < goal_deg:
                    degree += 1.0
                    pulse_width = 1500.0 + (degree * 10.0)
                    print(str(degree) + ',' + str(pulse_width))
                    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
                    if degree <= fst_goal:
                        time.sleep(mid_speed)
                    else:
                        time.sleep(slow_speed)
                end = time.time()
                print('周波数による制御で' + str(end - start) + '[sec]かかりました')
                print('mid_speed=' + str(mid_speed) + ',slow_speed=' + str(slow_speed))
                #-60degに戻す
                degree = -60
                pi.set_servo_pulsewidth(SERVO_PIN, 900.0)

        elif state == 1:
            print('state = 1:角度による制御です')
            #実験用
            mid_speed  = float(input('mid_degree :'))
            slow_speed = float(input('slow_degree:'))
            msec       = float(input('msec[sec]  :'))

            fst_goal = pre_deg + ((goal_deg - pre_deg) * FST)

            if (goal_deg > 60 or goal_deg < -60):
                print('60[deg]から-60[deg]で入力してください')
            else:
                start = time.time()
                #速度変数にあった角度調整
                while degree < goal_deg:
                    if degree <= fst_goal:
                        degree += mid_speed
                    else:
                        degree += slow_speed
                    pulse_width = 1500.0 + (degree * 10.0)
                    print(str(degree) + ',' + str(pulse_width))
                    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
                    time.sleep(msec)
                end = time.time()
                print('角度による制御で' + str(end - start) + '[sec]かかりました')
                print('mid_deg=' + str(mid_speed) + ',slow_deg=' + str(slow_speed) + ',msec=' + str(msec))
                #-60degに戻す
                degree = -60
                pi.set_servo_pulsewidth(SERVO_PIN, 900.0)


except KeyboardInterrupt:
    pass
pi.set_servo_pulsewidth(SERVO_PIN, 0.0)
#end of program
