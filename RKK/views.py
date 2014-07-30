# coding: utf-8
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import RequestContext
from sreda_mks.forms import UploadFileForm

def base_context(view):
    def new_view(request, *args, **kwargs):
        context = {}
        context.update(csrf(request))
        if request.POST:
            username = request.POST.get('login_username', '')
            password = request.POST.get('login_password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
        if request.user.is_authenticated():
            context['user_auth'] = request.user
        kwargs['base_context'] = RequestContext(request, context)
        context['form'] = UploadFileForm()
        return view(request, *args, **kwargs)
    return new_view


