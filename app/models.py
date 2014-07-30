# coding: utf-8
from django.db import models
# Create your models here.


class CM(models.Model):
    date = models.DateField(verbose_name=u'дата измерения', null=True)
    time_start = models.TimeField(verbose_name=u'время начала измерения', null=True)
    time_end = models.TimeField(verbose_name=u'время окончания измерения', null=True)
    raw_files = models.FileField(upload_to='raw_CM', verbose_name=u'необработанный файл')
    clean_files = models.FileField(upload_to='clean_CM', verbose_name=u'обработанный файл', null=True)
    clean_mod_files = models.FileField(upload_to='clean_CM/Модуль/', verbose_name=u'обработанный файл', null=True)
    plot_cmx = models.ImageField(upload_to='plot_CM/CMX/', verbose_name=u'графики файла', null=True)
    plot_cmy = models.ImageField(upload_to='plot_CM/CMY', verbose_name=u'графики файла', null=True)
    plot_cmz = models.ImageField(upload_to='plot_CM/CMZ/', verbose_name=u'графики файла', null=True)
    plot_mod = models.ImageField(upload_to='plot_CM/Модуль/', verbose_name=u'графики файла', null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            obj = CM.objects.get(id=self.id)
            if obj.raw_files.path != self.raw_files.path:
                obj.raw_files.delete()
            elif obj.clean_files.path != self.clean_files.path:
                obj.clean_files.delete()
            elif obj.clean_mod_files.path != self.clean_mod_files.path:
                obj.clean_mod_files.delete()
            elif obj.plot_cmx.path != self.plot_cmx.path:
                obj.plot_cmx.delete()
            elif obj.plot_cmy.path != self.plot_cmy.path:
                obj.plot_cmy.delete()
            elif obj.plot_cmz.path != self.plot_cmz.path:
                obj.plot_cmz.delete()
            elif obj.plot_mod.path != self.plot_mod.path:
                obj.plot_mod.delete()
        except (CM.DoesNotExist, ValueError):
            pass
        super(CM, self).save()

    def delete(self, using=None):
        try:
            obj = CM.objects.get(id=self.id)
            obj.raw_files.delete()
            obj.clean_files.delete()
            obj.clean_mod_files.delete()
            obj.plot_cmx.delete()
            obj.plot_cmy.delete()
            obj.plot_cmz.delete()
            obj.plot_mod.delete()
        except (CM.DoesNotExist, ValueError):
            pass
        super(CM, self).delete()

    def __unicode__(self):
        return u'{0}'.format(self.date.strftime('%d.%m.%y'))


class Kvaternion(models.Model):
    date = models.DateField(verbose_name=u'дата измерения', unique=True)
    time_start = models.TimeField(verbose_name=u'время начала измерения', unique=True)
    time_end = models.TimeField(verbose_name=u'время окончания измерения', unique=True)
    raw_files = models.FileField(upload_to='raw_KV', verbose_name=u'необработанный файл')
    clean_files = models.FileField(upload_to='clean_KV', verbose_name=u'обработанный файл', null=True)

    cm = models.OneToOneField('CM', unique=True)

    def __unicode__(self):
        return u'{0}'.format(self.date.strftime('%d.%m.%y'))


class GSW(models.Model):
    date = models.DateField(verbose_name=u'дата измерения', unique=True)
    time_start = models.TimeField(verbose_name=u'время начала измерения', unique=True)
    time_end = models.TimeField(verbose_name=u'время окончания измерения', unique=True)
    raw_files = models.FileField(upload_to='raw_GSW', verbose_name=u'необработанный файл')
    clean_files = models.FileField(upload_to='clean_GSW', verbose_name=u'обработанный файл', null=True)

    cm = models.OneToOneField('CM', unique=True)

    def __unicode__(self):
        return u'{0}'.format(self.date.strftime('%d.%m.%y'))
