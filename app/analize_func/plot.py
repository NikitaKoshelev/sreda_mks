#coding=utf-8
from os import mkdir
from numpy import loadtxt
from matplotlib import pyplot, dates, rcParams
from RKK.settings import MEDIA_ROOT
from data_interpol import *
rcParams['font.sans-serif'] = 'Arial'


def draw_plot(file_path=None, col_x_index=None, col_y_index=None,
              label_x=None, label_y=None, marker='', color='', linewidth=1.0,
              legend=False, step_grid=5, interpolation=False, quantity_interpolate_points=-1):

    if col_x_index is None or col_y_index is None or label_x is None or label_y is None or file_path is None:
        return u'Указаны не все параметры'

    col_x_index = int(col_x_index)
    col_y_index = int(col_y_index)
    column = loadtxt(file_path, converters={0: dates.strpdate2num('%H:%M:%S.%f')})
    x = column[:,col_x_index]
    y = column[:,col_y_index]
    fig = pyplot.figure(figsize=(16, 9))
    my_plot = fig.add_subplot(1, 1, 1)
    date = file_path.split('.')[0][-10:]
    pyplot.title(u'{0}'.format(date))
    pyplot.xlabel(u'{0}'.format(label_x))
    pyplot.ylabel(u'{0}'.format(label_y))
    if step_grid < 3:
        pyplot.xticks(rotation=90)
    elif 3 <= step_grid < 5:
        pyplot.xticks(rotation=20)
    else:
        pyplot.xticks(rotation=0)
    locator = dates.MinuteLocator(interval=step_grid)
    my_plot.xaxis.set_major_locator(locator)
    my_plot.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
    step_razr = len(y)//quantity_interpolate_points
    if interpolation is True:
        x1, y1 = spline(x, y, nest=quantity_interpolate_points, num_points=len(y))
        pyplot.plot(x1, y1, color=color, marker=marker, label=unicode(label_y), linewidth=linewidth)
    else:
        pyplot.plot(razrezh(x, step_razr), razrezh(y, step_razr), color=color, marker=marker, label=unicode(label_y), linewidth=linewidth)
    if legend is True:
        my_plot.legend(loc='best')
    my_plot.grid(True)
    try:
        mkdir(u'{0}/plot_CM/{1}/'.format(MEDIA_ROOT, label_y).replace('/', '\\'))
    except WindowsError:
        pass
    fh_path = u'{0}/plot_CM/{2}/{2}_{1}.png'.format(MEDIA_ROOT, date, label_y)
    fh = open(fh_path, 'wb')
    pyplot.savefig(fh, dpi=100, facecolor='w', edgecolor='w', pad_inches=0.1, bbox_inches="tight")
    #pyplot.show()
    pyplot.close()
    fh.close()
    return '/'.join(fh_path.split('/')[-3:])

#fh = open(ur'{0}/raw_CM/11-02-2014.txt'.format(MEDIA_ROOT), 'r')
#file_path = ur'{0}/clean_CM/mod/mod_11-02-2014.txt'.format(MEDIA_ROOT)
#draw_plot(file_path=file_path, col_x_index=0, col_y_index=3, label_x=u'Время', label_y=u'3', color='r', marker='',
#          legend=True, step_grid=1, interpolation=True, quantity_interpolate_points=-1)
#fh.close()