# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from RKK.views import base_context

from .views import *
admin.autodiscover()

urlpatterns = patterns('',
                       url(ur'^$', base_context(index)),
                       url(ur'^Загрузка_показаний_магнитометров/$', base_context(upload_CM)),
                       url(ur'^Просмотр_базы/$', base_context(list_db)),
                       url(ur'^Просмотр_базы/(?P<date>\d{4}-\d{2}-\d{2})/$', base_context(view_obj)),
                       url(ur'^Создание_графиков/Выбор_даты/$', base_context(select_date)),
                       url(ur'^Создание_графиков/(?P<date>\d{4}-\d{2}-\d{2})/(?P<param>Магнитометры|Кватернионы|Угловые скорости)/$', base_context(select_column)),

                       )
