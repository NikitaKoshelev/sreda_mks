#coding: utf-8
from datetime import datetime
import numpy as np
from matplotlib import pyplot, dates, rcParams
from data_interpol import *
from RKK.settings import MEDIA_ROOT

rcParams['font.sans-serif'] = 'Arial'


def test(raw_file=None):
    if raw_file is None:
        print u'Выберите файл'
    times, cmx, cmy, cmz, mod = np.loadtxt(raw_file, delimiter=';', unpack=True, converters={0: dates.strpdate2num('%H %M %S.%f')})
    print times, cmx, cmy, cmz, mod


def create_clean_files(raw_file=None, par1 = 5):
    if raw_file is None:
        print u'Выберите файл'
    #----------------------------------------------------------------------------------
    #Объявление переменных
    #----------------------------------------------------------------------------------
    cmx = []
    cmy = []
    cmz = []
    t1 = []
    t1s = []
    t2 = []
    t2s = []

    lst_t = []
    lst_t1 = []

    vrem = {}
    #----------------------------------------------------------------------------------
    #Формирование пременных из исходного файла
    #----------------------------------------------------------------------------------
    lines = raw_file.readlines()
    date_str = '.'.join(lines[0].strip().split()[-3:])
    date = datetime.strptime(date_str, 'date=%d.%m.%Y').date()

    for line in lines[4:]:
        vrem[line[:8].strip()] = line
    sort_for_time_path = ur'{0}\\raw_CM\\sort\\sort_{1}.txt'.format(MEDIA_ROOT, date.strftime('%d-%m-%Y'))
    sort_for_time = open(sort_for_time_path, 'w')
    for k in sorted(vrem.keys(), key=lambda x: datetime.strptime(date_str + 'T' + x.strip(), "date=%d.%m.%YT%H:%M:%S")):
        lst_t.append(k)
        sort_for_time.write(u'{0}'.format(vrem.get(k)))
    sort_for_time.close()

    for t in xrange(1, len(lst_t)):
        if (lst_t[t] != lst_t[t-1]):
            try:
                cmx.append(float(vrem.get(lst_t[t])[13:19].strip()))
                cmy.append(float(vrem.get(lst_t[t])[20:26].strip()))
                cmz.append(float(vrem.get(lst_t[t])[27:33].strip()))
            except ValueError:
                print t, lst_t[t]
            t1.append(vrem.get(lst_t[t])[:12].strip().replace(':', ' '))
            t1s.append(vrem.get(lst_t[t])[:5].strip())
            t2.append(vrem.get(lst_t[t])[34:47].strip().replace(':', ' '))
            t2s.append(vrem.get(lst_t[t])[34:39].strip())
            #print (t*100)//len(lst_t)
    #----------------------------------------------------------------------------------
    #Проверка условия, запись обработанных файлов
    #----------------------------------------------------------------------------------
    data_path = ur'{1}\clean_CM\cl_{0}.txt'.format(date.strftime('%d-%m-%Y'), MEDIA_ROOT)
    data_mod_path = ur'{1}\clean_CM\mod\mod_{0}.txt'.format(date.strftime('%d-%m-%Y'), MEDIA_ROOT)
    print data_path,data_mod_path
    data = open(data_path, 'w')
    data_mod = open(data_mod_path, 'w')

    dead_zone_x = min(cmx)
    dead_zone_y = min(cmy)
    dead_zone_z = min(cmz)
    dead_zone = abs(min(dead_zone_x, dead_zone_y, dead_zone_z))
    #x = float(input(u'Мертвая зона: {0}\n'
    #                u'Введите границу мертвой зоны (-{0};-{0}+X)U({0}-X;{0}).\n'
    #                u'X (рекомендуемое значение X=7) = '.format(dead_zone)))
    x = 6
    date_time, cmx_cl, cmy_cl, cmz_cl, mod_cl = [], [], [], [], []
    for i in xrange(1, len(cmx)):
        if t1s[i] == t2s[i]:
            if -dead_zone+x < cmx[i] < dead_zone-x \
                    and -dead_zone+x < cmy[i] < dead_zone-x  \
                    and -dead_zone+x < cmz[i] < dead_zone-x:

                if ((cmx[i] != cmx[i-1] or cmy[i] != cmy[i-1] or cmz[i] != cmz[i-1])
                    and cmx[i-1]-par1 < cmx[i] < cmx[i-1]+par1
                    and cmy[i-1]-par1 < cmy[i] < cmy[i-1]+par1
                    and cmz[i-1]-par1 < cmz[i] < cmz[i-1]+par1):

                    lst_t1.append(t1[i][:-4].replace(' ', ':'))
                    data.write('{0:13} {1:10} {2:10} {3:10}\n'.format(t1[i],
                                                                      cmx[i],
                                                                      cmy[i],
                                                                      cmz[i]))
                    mod = float(np.sqrt(cmx[i]**2+cmy[i]**2+cmz[i]**2))
                    data_mod.write('{0:13} {1:10.2f} {2:10.2f} {3:10.2f} {4:10.2f}\n'.format(t1[i].replace(' ',':')+'000',
                                                                       cmx[i],
                                                                       cmy[i],
                                                                       cmz[i],
                                                                       mod))
                    date_time.append(datetime.strptime(u'{0}T{1}000'.
                                                       format(date.strftime('%d-%m-%Y'), t1[i]),
                                                       u'%d-%m-%YT%H %M %S.%f'))
                    cmx_cl.append(cmx[i])
                    cmy_cl.append(cmy[i])
                    cmz_cl.append(cmz[i])
                    mod_cl.append(mod)
        progress = (i*100)//len(cmx)
        if progress != ((i+1)*100)//len(cmx):
            progress = ((i+1)*100)//len(cmx)
            print progress

    data.close()
    data_mod.close()
    try:
        min_time=lst_t1[0]
        max_time=lst_t1[-1]
        result = (('/'.join(sort_for_time_path.split('\\')[-3:]), '/'.join(data_path.split('\\')[-2:]), '/'.join(data_mod_path.split('\\')[-3:]), min_time, max_time, date),
                  (date_time, cmx_cl, cmy_cl, cmz_cl, mod_cl))
    except IndexError:
        pass
        result = ('{0:10} NO DANNYX\n'.format(date), None)
    return result


def draw(column=None, y=None, ):
    if column is None:
        return u'Нет значений для обработки'
    date_time, cmx, cmy, cmz, mod = column
    #print date_time, cmx, cmy, cmz, mod
    fh_set = set()

    if y is not None:
        y = str(y)
        if y == 'CMX':
            y_dict = {u'CMX': cmx}
        elif y == 'CMY':
            y_dict = {u'CMY': cmy}
        elif y == 'CMZ':
            y_dict = {u'CMZ': cmz}
        else:
            y_dict = {u'Модуль': mod}
    else:
        y_dict = {u'CMX': cmx, u'CMY': cmy, u'CMZ': cmz, u'Модуль': mod}
    j = 0
    for name, values in y_dict.items():
        fig = pyplot.figure(figsize=(16, 9))
        my_plot = fig.add_subplot(1, 1, 1)
        date = date_time[0].date()
        pyplot.title(u'{0}'.format(date.strftime('%d-%m-%Y')))
        pyplot.xlabel(u'Время')
        pyplot.ylabel(u'{0}'.format(name))
        locator = dates.MinuteLocator(interval=1)
        pyplot.xticks(rotation=90)
        my_plot.xaxis.set_major_locator(locator)
        my_plot.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
        #pyplot.plot(date_time, values, label=u'Оригинал')
        values_float = []
        for i, val in enumerate(values, start=1):
            values_float.append(float(val))
        SP = len(date_time[50-1:])
        y = movingaverage(values_float, 50)
        #pyplot.plot(date_time[-SP:], y[-SP:], 'r', linewidth=5)
        y1 = ExpMovingAverage(values_float, 12)
        SP1 = len(date_time[12-1:])
        #pyplot.plot(date_time[-SP1:], y1[-SP1:], 'r', linewidth=3)
        date_num = dates.date2num(date_time)
        j += 0.5
        print (j*100)//len(y_dict.keys())
        y1 = cubic_spline(date_num, values_float, date_num[::25])
        y2 = interpolate_1d(date_num, values_float, date_num[::50])
        pyplot.plot(date_num[::50], y2, 'g', linewidth=2, label=u'1-D интерполяция')
        pyplot.plot(date_num[::25], y1, 'y', linewidth=2, label=u'Кубический сплайн')
        my_plot.legend(loc='best')
        my_plot.grid(True)
        fh_path = u'{0}\plot_CM\{2}\{2}_{1}.png'.format(MEDIA_ROOT, date.strftime('%d-%m-%Y'), name)
        fh = open(fh_path, 'wb')
        pyplot.savefig(fh, dpi=300, facecolor='w', edgecolor='w', pad_inches=0.1, bbox_inches="tight")
        fh.close()
        pyplot.close()
        fh_set.add('/'.join(fh_path.split('\\')[-3:]))
        j += 0.5
        print (j*100)//len(y_dict.keys())
    return fh_set


#print(MEDIA_ROOT)
#fh = open(ur'{0}/clean_CM/mod/mod_11-02-2014.txt'.format(MEDIA_ROOT), 'r')
#fh = open(ur'{0}/raw_CM/15-09-2013.txt'.format(MEDIA_ROOT), 'r')
#test(fh)
#create_clean_files(fh)
#fh.close()
