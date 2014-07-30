#coding: utf-8
from datetime import datetime
from matplotlib import pyplot, dates
import math
from RKK.settings import MEDIA_ROOT
from decimal import Decimal, getcontext
from django.contrib import messages
getcontext().prec = 2


class CM():
    def __init__(self, raw_file=None):
        self.raw_file = raw_file.readlines()
        self.date_time = []
        self.cmx = []
        self.cmy = []
        self.cmz = []
        self.mod = []
        self.date = None

    def create_clean_files(self, par1 = 2):
        #----------------------------------------------------------------------------------
        #Объявление переменных
        #----------------------------------------------------------------------------------
        cmx, cmy, cmz, t1, t1s, t2, t2s, lst_t, lst_t1 = [], [], [], [], [], [], [], [], []

        vrem = {}
        #----------------------------------------------------------------------------------
        #Формирование пременных из исходного файла
        #----------------------------------------------------------------------------------
        date_str = '.'.join(self.raw_file[0].strip().split()[-3:])
        self.date = datetime.strptime(date_str, 'date=%d.%m.%Y').date()

        for line in self.raw_file[4:]:
            vrem[line[:8].strip()] = line

        sort_for_time = open(ur'{0}\\raw_CM\\sort\\sort_{1}.txt'.format(MEDIA_ROOT, self.date.strftime('%d-%m-%Y')), 'w')
        for k in sorted(vrem.keys(), key=lambda x: datetime.strptime(date_str + 'T' + x.strip(), "date=%d.%m.%YT%H:%M:%S")):
            lst_t.append(k)
            sort_for_time.write(u'{0}'.format(vrem.get(k)))
        sort_for_time.close()

        for t in xrange(1, len(lst_t)):
            if (lst_t[t] != lst_t[t-1]):
                try:
                    cmx.append(Decimal(vrem.get(lst_t[t])[13:19].strip()))
                    cmy.append(Decimal(vrem.get(lst_t[t])[20:26].strip()))
                    cmz.append(Decimal(vrem.get(lst_t[t])[27:33].strip()))
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
        data_path = ur'{1}\\clean_CM\\cl_{0}.txt'.format(self.date.strftime('%d-%m-%Y'), MEDIA_ROOT)
        data_mod_path = ur'{1}\\clean_CM\\mod\\mod_{0}.txt'.format(self.date.strftime('%d-%m-%Y'), MEDIA_ROOT)
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
                        koren = Decimal(math.sqrt(cmx[i]**2+cmy[i]**2+cmz[i]**2))
                        data_mod.write('{0:13} {1:10} {2:10} {3:10} {4:10.2f}\n'.format(t1[i],
                                                                                    cmx[i],
                                                                                    cmy[i],
                                                                                    cmz[i],
                                                                                    koren))
                        self.date_time.append(datetime.strptime(u'{0}T{1}000'.
                                                                format(self.date.strftime('%d-%m-%Y'), t1[i]),
                                                                u'%d-%m-%YT%H %M %S.%f'))
                        self.cmx.append(cmx[i])
                        self.cmy.append(cmy[i])
                        self.cmz.append(cmz[i])
                        self.mod.append(koren)
            progress = (i*100)//len(cmx)
            if progress != ((i+1)*100)//len(cmx):
                progress = ((i+1)*100)//len(cmx)
                print progress

        data.close()
        data_mod.close()
        try:
            min_time=lst_t1[0]
            max_time=lst_t1[-1]
            result = '/'.join(data_path.split('\\')[-2:]), '/'.join(data_mod_path.split('\\')[-3:]), min_time, max_time, self.date
        except IndexError:
            pass
            #result ='{0:10} NO DANNYX\n'.format((self.date[len('.\\Magn\\Raw\\'):-4]))
        return result

    def create_clean_files_backup(self, a=0.8):

        line_list = []
        cmy = []
        cmz = []
        t1 = []
        t2 = []

        a = Decimal(str(a))

        date_str = '.'.join(self.raw_file[0].strip().split()[-3:])
        self.date = datetime.strptime(date_str, 'date=%d.%m.%Y')

        data_path = ur'{1}\\clean_CM\\cl_{0}.txt'.format(self.date.strftime('%d-%m-%Y'), MEDIA_ROOT)
        data_mod_path = ur'{1}\\clean_CM\\mod\\mod_{0}.txt'.format(self.date.strftime('%d-%m-%Y'), MEDIA_ROOT)
        data = open(data_path, 'w')
        data_mod = open(data_mod_path, 'w')

        cmx_set, cmy_set, cmz_set = set(), set(), set()
        dead_zone = 56.0

        for lino, line in enumerate(self.raw_file[4:], start=1):
            t1_str, cmx_str, cmy_str, cmz_str, t2_str = line.strip().split()[:-1]

            try:
                t1_str, cmx_str, cmy_str, cmz_str, t2_str = (t1_str.replace(':', ' ').strip(),
                                                             Decimal(cmx_str.strip()),
                                                             Decimal(cmy_str.strip()),
                                                             Decimal(cmz_str.strip()),
                                                             t2_str.strip('*').replace(':', ' ').strip())

                if (-dead_zone+7 <= cmx_str <= dead_zone-7 and
                    -dead_zone+7 <= cmy_str <= dead_zone-7 and
                    -dead_zone+7 <= cmz_str <= dead_zone-7):

                    line_list.append((t1_str, cmx_str, cmy_str, cmz_str, t2_str))
            except ValueError:
                pass
            progress = ((lino-1)*100)//len(self.raw_file[4:])
            if progress != (lino*100)//len(self.raw_file[4:]):
                progress = (lino*100)//len(self.raw_file[4:])
                print progress

        for lino, line_tuple in sorted(enumerate(line_list[1:], start=1),
                                       key=lambda (i, v): datetime.strptime('{0}000'.format(v[0]),
                                                                            '%H %M %S.%f').time()):

            t1_str, cmx_str, cmy_str, cmz_str, t2_str = line_tuple
            t1_last, cmx_last, cmy_last, cmz_last, t2_last = line_list[lino-1]
            
            if (-dead_zone+7 <= cmx_str <= dead_zone-7 and
                -dead_zone+7 <= cmy_str <= dead_zone-7 and
                -dead_zone+7 <= cmz_str <= dead_zone-7):
               # print cmx_str, cmy_str, cmz_str
                if t1_str[:-4] == t1_last[:-4]:
                    cmx_set.add(cmx_str)
                    cmx_str = sum(cmx_set)/(len(cmx_set) if len(cmx_set) != 0 else 1)
                    cmy_set.add(cmy_str)
                    cmy_str = sum(cmy_set)/(len(cmy_set) if len(cmy_set) != 0 else 1)
                    cmz_set.add(cmz_str)
                    cmz_str = sum(cmz_set)/(len(cmz_set) if len(cmz_set) != 0 else 1)
                else:
                    cmx_set, cmy_set, cmz_set = set(), set(), set()

                if t1_str[:-7] == t2_str[:-7] and t1_str[:-4] != t1_last[:-4]:

                    if (((cmx_str != cmx_last) or (cmy_str != cmy_last) or (cmz_str != cmz_last)) and
                            ((cmx_last-3 <= cmx_str <= cmx_last+3) and
                             (cmy_last-3 <= cmy_str <= cmy_last+3) and
                             (cmz_last-3 <= cmz_str <= cmz_last+3))):

                        self.date_time.append(datetime.strptime(u'{0}T{1}000'.
                                                                format(self.date.strftime('%d-%m-%Y'), t1_str),
                                                                u'%d-%m-%YT%H %M %S.%f'))
                        #cmx_str = a * cmx_str + (Decimal('1.0') - a) * cmx_last
                        #cmy_str = a * cmy_str + (Decimal('1.0') - a) * cmy_last
                        #cmz_str = a * cmz_str + (Decimal('1.0') - a) * cmz_last
                        mod = Decimal('{0}'.format(math.sqrt(cmx_str**2+cmy_str**2+cmz_str**2)))

                        self.cmx.append(cmx_str)
                        self.cmy.append(cmy_str)
                        self.cmz.append(cmz_str)
                        self.mod.append(mod)

                        data.write('{0:13} {1:10.2f} {2:10.2f} {3:10.2f}\n'.format(t1_str,
                                                                                   cmx_str,
                                                                                   cmy_str,
                                                                                   cmz_str))

                        data_mod.write('{0:13} {1:10.2f} {2:10.2f} {3:10.2f} {4:10.2f}\n'.format(t1_str,
                                                                                                 cmx_str,
                                                                                                 cmy_str,
                                                                                                 cmz_str,
                                                                                                 mod))
            print (lino*100)//len(self.raw_file[4:])

        data.close()
        data_mod.close()

        try:
            time_min, time_max = min(self.date_time), max(self.date_time)
            return '/'.join(data_path.split('\\')[-2:]), '/'.join(data_mod_path.split('\\')[-3:]), time_min, time_max, self.date
        except ValueError:
            return u'В файле отсутствуют показания магнитометров'

    def draw(self, a=0.5, axis_y=None):
        fh_set = set()
        a = Decimal(str(a))

        if axis_y is not None:
            axis_y = str(axis_y)
            if axis_y == 'CMX':
                axis_y_dict = {u'CMX': self.cmx}
            elif axis_y == 'CMY':
                axis_y_dict = {u'CMY': self.cmy}
            elif axis_y == 'CMZ':
                axis_y_dict = {u'CMZ': self.cmz}
            else:
                axis_y_dict = {u'Модуль': self.mod}
        else:
            axis_y_dict = {u'CMX': self.cmx, u'CMY': self.cmy, u'CMZ': self.cmz, u'Модуль': self.mod}
        j = 0
        for name, values in axis_y_dict.items():
            #res = []
            #for i in xrange(len(values)):
            #    if i == 0:
            #        res.append(values[i])
            #    else:
            #        ema = a * values[i] + (Decimal('1.0') - a) * res[-1]
            #        res.append(ema)
            fig = pyplot.figure(figsize=(16, 9))
            my_plot = fig.add_subplot(1, 1, 1)
            date = self.date_time
            pyplot.plot(date, values)
            pyplot.title(u'{0}'.format(self.date.strftime('%d-%m-%Y')), family="verdana")
            pyplot.xlabel(u'Время',  family="verdana")
            pyplot.ylabel(u'{0}'.format(name), family="verdana")
            locator = dates.MinuteLocator(interval=1)
            pyplot.xticks(rotation=90)
            my_plot.xaxis.set_major_locator(locator)
            my_plot.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
            my_plot.grid(True)
            fh_path = u'{0}\\plot_CM\\{2}\\{2}_{1}.png'.format(MEDIA_ROOT, self.date.strftime('%d-%m-%Y'), name)
            fh = open(fh_path, 'wb')
            pyplot.savefig(fh, dpi=100, facecolor='w', edgecolor='w', pad_inches=0.1, bbox_inches="tight")
            fh.close()
            pyplot.close()
            fh_set.add('/'.join(fh_path.split('\\')[-3:]))
            j += 1
            print (j*100)//len(axis_y_dict.keys())
        return fh_set


#print(MEDIA_ROOT)
#fh = open(ur'{0}/raw_CM/11-02-2014.txt'.format(MEDIA_ROOT), 'r')
#fh = open(ur"F:/Users/NikitaKoshelev/Desktop/Raw/MAGN/2-11-2013.txt")
#
#test = CM(raw_file=fh)
#test.magn()
#test.draw()
#fh.close()
