from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^ad/', 'whopaid_api.views.fp_search'),
        )
