from django.template import RequestContext
from django.shortcuts import render_to_response


def set_client(request):
    user_agent = request.META['HTTP_USER_AGENT']
    if user_agent == 'com.sunlightfoundation.com.adhawk.android':
        return 'android'
    elif user_agent == 'com.sunlightfoundation.com.adhawk.ios':
        return 'ios'
    else:
        return user_agent

def about(request):
    client = set_client(request)
    c = RequestContext({
            'client' : client,
            })
    return render_to_response('whopaid/about.html',c)
