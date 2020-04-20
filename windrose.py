# -*- encoding: utf-8 -*-
'''
@Author: sandwich
@Date: 2020-03-13 18:44:34
@LastEditTime: 2020-03-13 18:44:34
@LastEditors: sandwich
@Description: In User Settings Edit
@FilePath: /VisualData/windrose.py
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def maker(s, sequence):
    for i, val in enumerate(sequence):
        if s <= sequence[i+1]:
            return val

if __name__ == "__main__":
    file = r'e:\公司文档\自动化\自产雷达\20年2月1日0时至20年2月29日23时气象参数小时值（Src）(3).xls'
    df = pd.read_excel(file)
    ds = df[['风向(deg)', '风速(m/s)', 'PM2.5']].iloc[:115, :]
    deg = np.radians(ds['风向(deg)'].to_numpy())
    ds['风向(deg)'] = deg
    ds['PM2.5'] = ds['PM2.5'].apply(lambda s: float(s))
    v = ds['风速(m/s)']
    d = ds['风向(deg)']
    speed = np.linspace(v.min(), v.max(), endpoint=True, num=16)
    deg = np.linspace(0, 2*np.pi, endpoint=True, num=32)

    ds['风速(m/s)'] = ds['风速(m/s)'].apply(maker, sequence=speed)
    ds['风向(deg)'] = ds['风向(deg)'].apply(maker, sequence=deg)
    dt = pd.pivot_table(ds, values='PM2.5', index='风速(m/s)', columns='风向(deg)')
    dt.fillna(0, inplace=True)
    dt[2*np.pi] = 0
    dt = dt.reindex(columns=deg, fill_value=0)
    theta, r = np.meshgrid(dt.columns, dt.index)
    ax = plt.subplot(projection='polar')
    ax.set_theta_zero_location("N")
    ax.set_theta_direction('clockwise')
    pos = ax.contourf(theta, r, dt.to_numpy(), cmap='jet')
    plt.colorbar(pos, ax=ax)
    plt.show()