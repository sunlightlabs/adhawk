from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^ad/', 'whopaid_api.views.fp_search'),
        url(r'^site_mapping/', 'whopaid_api.views.site_mapping'),
        )
