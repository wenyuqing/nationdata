#from download import Downloader
from data import Database
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    #选做任务1：年末总人口+年末男性总人口+年末女性总人口
    database1 = Database('summary.db','A030101_sj', [], [], {}, '[{"wdcode":"sj","valuecode":"LAST20"}]')
    database1.save()
    database2 = Database('man.db','A030102_sj', [], [], {}, '[{"wdcode":"sj","valuecode":"LAST20"}]')
    database2.save()
    database3 = Database('woman.db','A030103_sj', [], [], {}, '[{"wdcode":"sj","valuecode":"LAST20"}]')
    database3.save()

    malerate = []
    femalerate = []
    for i in range(20):
        malerate.append(float(database2.data_list[i]/database1.data_list[i])*100)
        femalerate.append(float(database3.data_list[i]/database1.data_list[i])*100)

    # 必做题目:查询森林火灾次数+严重程度
    #森林火灾次数
    database4 = Database('fire.db', 'A0C0E01_sj', [], [], {}, '[{"wdcode":"zb","valuecode":"A0C0E"}]')
    database4.save()
    del database4.year_list[9]
    del database4.data_list[9]
    #一般火灾次数
    database5 = Database('fire1.db', 'A0C0E02_sj', [], [], {}, '[{"wdcode":"zb","valuecode":"A0C0E"}]')
    database5.save()
    del database5.year_list[9]
    del database5.data_list[9]
    #较大火灾次数
    database6 = Database('fire2.db', 'A0C0E03_sj', [], [], {}, '[{"wdcode":"zb","valuecode":"A0C0E"}]')
    database6.save()
    del database6.year_list[9]
    del database6.data_list[9]
    #重大火灾次数
    database7 = Database('fire3.db', 'A0C0E04_sj', [], [], {}, '[{"wdcode":"zb","valuecode":"A0C0E"}]')
    database7.save()
    del database7.year_list[9]
    del database7.data_list[9]
    #特别重大火灾次数
    database8 = Database('fire4.db', 'A0C0E05_sj', [], [], {}, '[{"wdcode":"zb","valuecode":"A0C0E"}]')
    database8.save()
    del database8.year_list[9]
    del database8.data_list[9]

    # 画图*****************
    #人口统计图
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(14,22))
    plt.suptitle(u'年末人口统计图', fontsize=16)

    # 子图一
    plt.subplot(311)
    plt.xlabel(u'年份')
    plt.ylabel(u'万人')
    plt.title(u'年末总人口')
    plt.bar(database1.year_list, database1.data_list)
    #plt.grid(True)

    # 子图二
    plt.subplot(312)
    plt.xlabel(u'年份')
    plt.ylabel(u'万人')
    plt.title(u'年末总人口')
    plt.plot(database2.year_list, database2.data_list, marker='o', label='男性', linewidth=3)
    plt.plot(database3.year_list, database3.data_list, marker='o', label='女性', linewidth=3, color='red')
    plt.legend()
    plt.grid(True)

    # 子图三
    plt.subplot(313)
    plt.xlabel(u'年份')
    plt.ylabel(u'百分比%')
    plt.title(u'男女性人口占比')
    plt.plot(database2.year_list, malerate, marker='o', label='男性', linewidth=3)
    plt.plot(database3.year_list, femalerate, marker='o', label='女性', linewidth=3, color='red')
    plt.legend()
    plt.grid(True)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=1, hspace=0.4)

    # 森林火灾统计图
    fig=plt.figure(figsize=(14,22))
    plt.suptitle(u'森林火灾统计图', fontsize=16)
    #子图一
    plt.subplot(311)
    plt.xlabel(u'年份')
    plt.ylabel(u'次')
    plt.title(u'森林火灾次数')
    plt.plot(database4.year_list, database4.data_list,marker='o')
    plt.grid(True)

    #子图二
    fig1=plt.subplot(312)
    plt.xlabel(u'年份')
    plt.ylabel(u'次')
    plt.title(u'火灾次数')
    barwidth=0.2
    index = np.arange(9)
    xmajorlocator = MultipleLocator(1)  # 配置刻度
    ymajorlocator = MultipleLocator(1000)
    fig1.xaxis.set_major_locator(xmajorlocator)
    fig1.yaxis.set_major_locator(ymajorlocator)

    plt.bar(index+2009, database5.data_list, width=barwidth,label='一般火灾', color='red')
    plt.bar(index+2009+barwidth, database6.data_list, width=barwidth,label='较大火灾', color='blue')
    plt.legend()
    plt.grid(True)

    #子图三
    fig2 = plt.subplot(313)
    plt.xlabel(u'年份')
    plt.ylabel(u'次')
    plt.title(u'火灾次数')
    barwidth = 0.2
    index = np.arange(9)
    xmajorlocator = MultipleLocator(1)  # 配置刻度
    ymajorlocator = MultipleLocator(5)
    fig2.xaxis.set_major_locator(xmajorlocator)
    fig2.yaxis.set_major_locator(ymajorlocator)

    plt.bar(index + 2009, database7.data_list, width=barwidth, label='重大火灾', color='yellow')
    plt.bar(index + 2009 + barwidth, database8.data_list, width=barwidth, label='特别重大火灾', color='green')
    plt.legend()
    plt.grid(True)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=1, hspace=0.4)

    plt.show()