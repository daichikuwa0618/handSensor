# -*- coding: utf-8 -*-
#!/usr/bin/env python

#ロボットハンドの速度制御をするプログラム
#目標角度を設定して、開くのか閉じるのかを指定することでハンドの制御を行う
#テスト動作モードは速度の制御は行わず、位置決め制御のみを行う
#速度制御について。角度を固定して周期を変更するのか、周期は固定して角度を変更するのか処理時間やトルクなどを計測する必要あり。

import pigpio
import time
from time import sleep

pi = pigpio.pi()

#==========定数==========#
SERVO_PIN = 15
FST       = 0.5
SND       = 0.75

#==========変数宣言==========#
#処理時間計測用
start       = 0.0
end         = 0.0
#開閉の判別
state       = 0 #0:OPEN 1:GRIP
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
pulse_width = 1500.0 #1500:0deg 2100:60deg 900:-60deg(ccw:正)

#0degに設定
pi.set_servo_pulsewidth(SERVO_PIN, 1500)

try:
    while True:
        pre_deg  = goal_deg
        degree   = pre_deg
        goal_deg = float(input('目標角度を入力してください(-60deg to 60deg)'))
        state    = int(input('開く:0 閉じる:1 テスト動作:2 いずれかを入力:'))
        #テスト動作
        if state == 2:
            pulse_width = 1500.0 + (goal_deg * 10.0)
            pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
        #通常動作
        #開く動作(ゆっくりから速く)
        #パルスは小さくなる方と仮定
        elif state == 0:
            #実験用
            mid_speed  = float(input('mid_speed :'))
            slow_speed = float(input('slow_speed:'))

            fst_goal = pre_deg + ((goal_deg - pre_deg) * (1 - SND))
            snd_goal = pre_deg + ((goal_deg - pre_deg) * (1 - FST))

            if (goal_deg > 60 or goal_deg < -60):
                print('60[deg]から-60[deg]で入力してください')
            else:
                start = time.time()
                #速度変数にあった角度調整
                while degree > snd_goal:
                    degree -= 1.0
                    pulse_width = 1500.0 + (degree * 10.0)
                    print(str(degree) + ',' + str(pulse_width))
                    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
                    if degree >= fst_goal:
                        time.sleep(slow_speed)
                    else:
                        time.sleep(mid_speed)

                pulse_width = 1500.0 + (goal_deg * 10.0)
                pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
                end = time.time()
                print(str(end - start) + '[sec]かかりました')

        #閉じる動作(速くからゆっくり)
        #パルスは大きくなる方と仮定
        elif state == 1:
            #実験用
            mid_speed  = float(input('mid_speed :'))
            slow_speed = float(input('slow_speed:'))

            fst_goal = pre_deg + ((goal_deg - pre_deg) * FST)
            snd_goal = pre_deg + ((goal_deg - pre_deg) * SND)

            if (goal_deg > 60 or goal_deg < -60):
                print('60[deg]から-60[deg]で入力してください')
            else:
                start = time.time()
                degree = fst_goal
                pulse_width = 1500.0 + (degree * 10.0)
                pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
                #速度変数にあった角度調整
                while degree < goal_deg:
                    degree += 1.0
                    pulse_width = 1500.0 + (degree * 10.0)
                    print(str(degree) + ',' + str(pulse_width))
                    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
                    if degree <= snd_goal:
                        time.sleep(mid_speed)
                    else:
                        time.sleep(slow_speed)
                end = time.time()
                print(str(end - start) + '[sec]かかりました')
        else:
            print('指定条件エラー')
except KeyboardInterrupt:
    pass
pi.set_servo_pulsewidth(SERVO_PIN, 0.0)

#end of program
