#根据相应的算法，将常规5参数据进行归一化处理，计算特征值

def process1(para):
    print('开始处理数据：')
    df = para

    #进行数据的初步处理，提取数据，规整
    df2 = df.iloc[:,1:]
    df2.columns  = ['SO2','NO2','PM10','CO','PM2.5']
    for i in range(5):
        df2.iloc[:, i] = pd.to_numeric(df2.iloc[:, i], errors='coerce')

    df2.iloc[:,2] = df2.iloc[:,2] - df2.iloc[:,4]
    df2.iloc[:,3] = df2.iloc[:,3] * 1000

    #进行相应的算法处理
    df3 = df2.copy()
    num = df3.columns
    df3['total'] = df3.sum(axis=1)

    # 进行归一化处理
    for i in num:
        df3['{}-归一化处理'.format(i)] = df3.loc[:, i] / df3.loc[:, 'total']

    # 计算出特征值
    for i in num:
        df3['{}-特征值'.format(i)] = df3['{}-归一化处理'.format(i)] / df3['{}-归一化处理'.format(i)].mean(axis=0)

    # 计算出上限
    for i in num:
        df3['{}-上限'.format(i)] = 1 + ((df3['{}-特征值'.format(i)].std(ddof=0) / df3['{}-特征值'.format(i)].mean(axis=0)))

    # 计算下限
    for i in num:
        df3['{}-下限'.format(i)] = 1 - (df3['{}-特征值'.format(i)].std(ddof=0) / df3['{}-特征值'.format(i)].mean(axis=0))


    df3.insert(loc = 0,column = df.columns[0],value = df.iloc[:,0])


    print('数据处理结束')
    return df3

#依据相应的算法，处理待测数据
def process2(data,background):

    ce = data.copy()
    df = background.copy()

    #数据前处理,规整数据
    ce1 = ce.iloc[:, 1:]
    ce1.columns = ['SO2', 'NO2', 'PM10', 'CO', 'PM2.5']

    for i in range(5):
        ce1.iloc[:, i] = pd.to_numeric(ce1.iloc[:, i], errors='coerce')
    ce1.iloc[:, 2] = ce1.iloc[:, 2] - ce1.iloc[:, 4]
    ce1.iloc[:, 3] = ce1.iloc[:, 3] * 1000

    #开始进行相应的算法
    ce2 = ce1.copy()
    num = ['SO2','NO2','PM10','CO','PM2.5']
    ce2['total'] = ce2.sum(axis=1)

    #进行归一化处理
    for i in num:
        ce2['{}-归一化处理'.format(i)] = ce2.loc[:, i] / ce2.loc[:, 'total']

    #计算特征值
    for i in num:
        ce2['{}-特征值'.format(i)] = ce2['{}-归一化处理'.format(i)] /df['{}-归一化处理'.format(i)].mean(axis = 0)

    ce2.insert(loc=0, column=ce.columns[0], value=ce.iloc[:, 0])

    return ce2


def plot_ladar(values,standards,limit_1,limit_2,labels=None, _max=None):
    # 定义颜色
    line_color = np.array([215, 215, 215])/255
    d_color = np.array([47, 126, 216])/255
    # 过滤处理
    max = values.copy()
    max.extend(limit_1)
    if not labels:
        labels = range(len(values))
    if not _max:
        _max = np.max(max)

    n = len(values)
    angles = np.concatenate((np.linspace(0, 2*np.pi, n, endpoint=False), [0]))

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for ang in angles:
        ax.plot([ang]*2, [0, _max], '-', c=line_color)
    # -------绘制边界------- #
    tick = 3
    for i in range(tick):
        ax.plot(angles, [_max*(1/tick)*(i+1)]*(n+1), c = line_color)
    # -------绘制数据------- #

    ax.plot(angles, standards+[standards[0]], "-", c = 'k',label = '标准值')
    ax.plot(angles, limit_1 + [limit_1[0]], "--", color='r',label = '上限')
    ax.plot(angles, limit_2 + [limit_2[0]], "--", c='g',label = '下限')
    ax.plot(angles, values + [values[0]], "-", c='orange', linewidth=3, label='特征值')

    plt.legend(loc='upper right', frameon=False, ncol = 6,bbox_to_anchor=(1.3, 0))
    ax.set_thetagrids(angles * 180 / np.pi, labels) # 设置显示的角度，将弧度转换为角度

    ax.set_theta_zero_location('N')        # 设置极坐标的起点（即0°）在正北方向，即相当于坐标轴逆时针旋转90°
    ax.spines['polar'].set_visible(False)  # 不显示极坐标最外圈的圆
    ax.grid(False)                         # 不显示默认的分割线
    ax.set_yticks([])# 不显示坐标间隔
    return plt

#特征雷达图2.xls
if __name__ == '__main__':
    print('开始导入模块')

    import numpy as np
    import pandas as pd
    import os
    import sys
    import matplotlib.pyplot as plt

    '''设置允许中文绘图'''
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams.update({'font.size': 15})


    #设置程序属性和输出属性
    path_file = os.path.abspath('main.py')
    path_file2 = os.path.dirname(path_file)
    os.chdir(path_file2)
    if not os.path.exists((str(path_file2) + str('\\处理后结果'))):
        os.makedirs((str(path_file2) + str('\\处理后结果')))


    #开始判断是够采用背景数据
    back = input('是否有背景数据，是请按1，否请按0：')

    #不采用背景数据绘制雷达图
    if back == '0':
        print('开始导入数据')
        name1 = str(input('请输入需要处理的文件的名称（包含拓展名）：'))

        try:
            df = pd.read_excel(name1)
        except OSError:
            print('文件名错误，请重新开始')
            input('<请按enter键重新开始>')
            sys.exit()

        try:
            df3 = process1(df)
            df3.to_excel('处理后结果\\处理后归一化数据.xlsx', index=None, encoding='utf-8')
        except ValueError:
            print('文格式错误，请重新开始')
            input('<请按enter键重新开始>')
            sys.exit()

        label1 = ['SO2', 'NO2', '粗颗粒物', 'CO', 'PM2.5']

        a = input('1、全部出图，2、选择性出图  如（选择全部出图按1）')
        standards = list([1, 1, 1, 1, 1])
        limit_1 = list(df3.iloc[1, 17:22])
        limit_2 = list(df3.iloc[1, 22:])

        if a == '1' :
            for i in np.arange(len(df3.index)):
                values = list(df3.iloc[i, 12:17])
                p = plot_ladar(values,standards,limit_1, limit_2,labels=label1)
                # p.show()
                plt.savefig('处理后结果\%s.png' % (i + 2))
                plt.close()

            input('<请按enter键退出>')
            sys.exit()
        #
        elif a == '2':
            while True:

                hang = int(input('请输入所需数据所在的行数（如：6）：')) - 2

                if hang >=0 and (hang < df3.shape[0]):
                    values = list(df3.iloc[hang,12:17])
                    p = plot_ladar(values,standards,limit_1, limit_2,labels=label1)
                    p.show()
                else:
                    print('所需数据所在行错误，请重新输入')
        else:
            print('输入错误！！')

    #采用背景数据，然后绘制雷达图
    if back == '1':
        print('开始导入数据')
        name1 = str(input('请输入背景文件名称（包含拓展名）：'))

        try:
            df = pd.read_excel(name1)
        except OSError:
            print('背景文件名错误，请重新开始')
            input('<请按enter键重新开始>')
            sys.exit()

        try:
            df3 = process1(df)
            df3.to_excel('处理后结果\\处理后背景数据.xlsx', index=None, encoding='utf-8')
        except ValueError:
            print('背景文格式错误，请重新开始')
            input('<请按enter键重新开始>')
            sys.exit()

        name2 = str(input('请输入待处理数据文件名称（包含拓展名）：'))
        try:
            ce = pd.read_excel(name2)
        except OSError:
            print('文件名错误，请重新开始')
            input('<请按enter键重新开始>')
            sys.exit()

        try:
            ce2 = process2(ce,df3)
            ce2.to_excel('处理后结果\\处理后数据.xlsx', index=None, encoding='utf-8')
        except ValueError:
            print('文格式错误，请重新开始')
            input('<请按enter键重新开始>')
            sys.exit()

        a = input('1、全部出图，2、选择性出图  如（选择全部出图按1）：')
        standards = list([1, 1, 1, 1, 1])
        limit_1 = list(df3.iloc[1, 17:22])
        limit_2 = list(df3.iloc[1, 22:])
        label1 = ['SO2', 'NO2', '粗颗粒物', 'CO', 'PM2.5']

        if a == '1':
            for i in np.arange(len(ce2.index)):
                values = list(ce2.iloc[i, 12:17])
                p = plot_ladar(values, standards, limit_1, limit_2, labels=label1)
                # p.show()
                plt.savefig('处理后结果\%s.png' % (i + 2))
                plt.close()

            input('<请按enter键退出>')
            sys.exit()


        elif a == '2':


            while True:
                hang = int(input('请输入所需数据所在的行数（如：6）：')) - 2
                if hang >= 0 and (hang < ce2.shape[0]):

                    values = list(ce2.iloc[hang, 12:17])
                    p = plot_ladar(values, standards, limit_1, limit_2, labels=label1)
                    p.show()
                else:
                    print('所需数据所在行错误，请重新输入')
        else:
            print('输入错误！！')
    #
    #









