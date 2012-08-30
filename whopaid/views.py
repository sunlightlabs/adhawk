from django.template import RequestContext
from django.shortcuts import render_to_response

from knowledge_base.views import set_client

def about(request):
    client = set_client(request)
    print "user agent is",client
    c = RequestContext(request,{
            'client' : client,
            })
    return render_to_response('whopaid/about.html',c)

def no_match(request):
    client = set_client(request)
    c = RequestContext(request,{
            'client' : client,
            })
    return render_to_response('whopaid/no_match.html',c)

def landing_page(request):
    client = set_client(request)
    c = RequestContext(request,{
        'client' : client,
        })
    return render_to_response('whopaid/landing_page.html',c)

def glossary(request):
    client = set_client(request)
    c = RequestContext(request,{
            'client' : client,
            })
    return render_to_response('whopaid/glossary.html',c)
