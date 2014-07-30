# coding: utf-8
from django import forms
from .widgets import *
from .models import CM


class UploadFileForm(forms.Form):
    raw_files = forms.FileField(widget=MultiFileInput)


class Plot(forms.Form):
    labelX = forms.CharField()
    labelY = forms.CharField()
    color = forms.CharField()
    marker = forms.CharField()
    legend = forms.CharField()
    grid = forms.IntegerField()
    interpolation = forms.CharField()
    step = forms.IntegerField()
    linewidth = forms.FloatField()

class SelectFiles(forms.Form):
    date = forms.DateField()
    files = forms.CharField()