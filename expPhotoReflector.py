# -*- coding: utf-8 -*-
#!/usr/bin/env python

# フォトリフレクタの電圧距離特性を調べる実験

# ========== import ==========
from gpiozero import MCP3208
import time
from datetime import datetime

adc = MCP3208(channel = 0)

if __name__ == '__main__':
    try:
        with open("フォトリフレクタ電圧距離特性.txt", "a") as f:
            # 実験開始日時を書き込む
            f.write("====================\n" + str(datetime.now()) + "\n")

        # 最初と最後の距離
        while True:
            startDst = int(input("何mm から:"))
            endDst = int(input("何mm まで:"))
            if startDst > endDst:
                print("小さい方から大きい方へ測定しますのでもう一度")
            else:
                break

        # 分割する距離
        divDst = int(input("何mm 刻みで測定しますか:"))

        # nowDstに格納
        nowDst = startDst
        while nowDst < endDst:
            input(str(nowDst) + "[mm]です。設定したらreturnキーを押してください")
            with open("フォトリフレクタ電圧距離特性.txt", "a") as f:
                f.write(str(nowDst) + " " + str(adc.value) + "\n")
            nowDst = nowDst + divDst

    except KeyboardInterrupt:
        pass




