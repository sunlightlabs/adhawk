from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^ad/', 'adhawk_api.views.fp_search'),
        url(r'^site_mapping/', 'adhawk_api.views.site_mapping'),
        )
