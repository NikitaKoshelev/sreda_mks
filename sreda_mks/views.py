# coding: utf-8
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib import messages
from .forms import UploadFileForm, Plot, SelectFiles
from .models import CM, Kvaternion, GSW
from analize_func import func, plot
from RKK.settings import MEDIA_ROOT
# Create your views here.


def index(request, **kwargs):
    context = kwargs['base_context']
    return render_to_response('base.html', context)


def upload_CM(request, **kwargs):
    context = kwargs['base_context']
    if request.method == 'POST':
        context['form'] = UploadFileForm(request.POST, request.FILES)
        if context['form'].is_valid():
            result_create = func.create_clean_files(raw_file=request.FILES['raw_files'])
            if type(result_create) is unicode:
                messages.warning(request, result_create[0])
            else:
                raw_files, clean_files, clean_mod_files, time_start, time_end, date = result_create[0]

                instance = CM(date=date, time_start=time_start, time_end=time_end,
                              clean_files=clean_files, clean_mod_files=clean_mod_files, raw_files=raw_files)
                instance.save()
            context['form'] = UploadFileForm()
    else:
        context['form'] = UploadFileForm()
    return render_to_response('upload_result.html', context)


def list_db(request, **kwargs):
    context = kwargs['base_context']
    context['CMs'] = CM.objects.all().order_by('date')
    return render_to_response('list_db.html', context)


def select_date(request, **kwargs):
    context = kwargs['base_context']
    context['CMs'] = CM.objects.all().order_by('date')
    if request.method == 'POST':
        form = context['SelectFiles'] = SelectFiles(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            param = form.cleaned_data['files']
            return HttpResponseRedirect(u'/Среда-МКС/Создание_графиков/{0}/{1}/'.format(date.strftime('%Y-%m-%d'), param))
        else:
            print "Fail"
    else:
        context['SelectFiles'] = SelectFiles()
    return render_to_response('select_files.html', context)


def select_column(request, date, param, **kwargs):
    context = kwargs['base_context']
    if param == u'Магнитометры':
        obj = CM.objects.all().get(date=date)
        file_path = obj.clean_mod_files
        context['labels'] = {u'Время': 0, u'CMX': 1, u'CMY': 2, u'CMZ': 3, u'Модуль': 4}
    elif param == u'Кватернионы':
        obj = Kvaternion.objects.all().get(date=date)
        file_path = obj.clean_files
    else:
        obj = GSW.objects.all().get(date=date)
        file_path = obj.clean_files
    context['file'] = file_path
    context['date'] = obj.date
    context['param'] = param
    if request.method == 'POST':
        form = context['PlotForm'] = Plot(request.POST)
        if form.is_valid():
            color, grid, interpolation, labelX, labelY, legend, linewidth, marker, step = sorted(form.cleaned_data.items(), key=lambda x: x[0])
            color, grid, interpolation, labelX, labelY, legend, linewidth, marker, step = (color[1].split(':')[0].strip(),
                                                                                grid[1],
                                                                                True if interpolation[1] == u'True' else False,
                                                                                labelX[1],
                                                                                labelY[1],
                                                                                True if legend[1] == u'True' else False,
                                                                                linewidth[1],
                                                                                marker[1].split(':')[0].strip("'"),
                                                                                step[1])
            labelX_index = context['labels'][labelX]
            labelY_index = context['labels'][labelY]
            plot_CM = plot.draw_plot(file_path=MEDIA_ROOT+'/'+file_path.name, col_x_index=labelX_index, col_y_index=labelY_index, label_x=labelX, label_y=labelY,
                           color=color, marker=marker, legend=legend, linewidth=linewidth, step_grid=grid, interpolation=interpolation,
                           quantity_interpolate_points=step)
            file_path.close()
            if labelY == u'CMX':
                obj.plot_cmx = plot_CM
            elif labelY == u'CMY':
                obj.plot_cmy = plot_CM
            elif labelY == u'CMZ':
                obj.plot_cmz = plot_CM
            else:
                obj.plot_mod = plot_CM
            obj.save()
            return HttpResponseRedirect(u'/Среда-МКС/Просмотр_базы/{0}/'.format(date))

    return render_to_response('draw_plot.html', context)


def view_obj(request, date, **kwargs):
    context = kwargs['base_context']
    context['cm'] = CM.objects.all().get(date=date)
    return render_to_response('object.html', context)




