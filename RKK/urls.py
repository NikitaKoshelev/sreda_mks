# coding: utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RKK.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(ur'^admin/', include(admin.site.urls)),
    url(ur'^Среда-МКС/', include('sreda_mks.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
