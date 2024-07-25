#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'chengzhi'

from datetime import date
from tqsdk import TqApi, TqAuth, TqBacktest, TargetPosTask,TqSim,BacktestFinished
acc = TqSim()
'''
回测从 2018-05-01 到 2018-10-01
'''
# 在创建 api 实例时传入 TqBacktest 就会进入回测模式
api = TqApi(acc,backtest=TqBacktest(start_dt=date(2018, 5, 1), end_dt=date(2018, 10, 1)), auth=TqAuth("billin", "dnadna"))
# get m1901 5m KLine
klines = api.get_kline_serial("DCE.m1901", 5 * 60, data_length=15)
# 创建 m1901 的目标持仓 task，该 task 负责调整 m1901 的仓位到指定的目标仓位
target_pos = TargetPosTask(api, "DCE.m1901")


print(acc.tqsdk_stat)  # 回测时间内账户交易信息统计结果，其中包含以下字段
# 由于需要在浏览器中查看绘图结果，因此程序不能退出
while True:
    api.wait_update()
    if api.is_changing(klines):
        ma = sum(klines.close.iloc[-15:]) / 15
        print("Latest Price", klines.close.iloc[-1], "MA", ma)
        if klines.close.iloc[-1] > ma:
            print("Latest>MA: buy 5")
            # buy
            target_pos.set_target_volume(5)
        elif klines.close.iloc[-1] < ma:
            print("Latest<MA: balance")
            # balance
            target_pos.set_target_volume(0)
