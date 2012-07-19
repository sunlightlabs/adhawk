from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'whopaid.views.home', name='home'),
    # url(r'^whopaid/', include('whopaid.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin: 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include('whopaid_api.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    url(r'^ad/(?P<path>.*)$','knowledge_base.views.ad_profile'),
)
