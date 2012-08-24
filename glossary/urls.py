from django.conf.urls.defaults import *
from views import list

urlpatterns = patterns('',
    url(r'^$', list, name="glossary"),
)
