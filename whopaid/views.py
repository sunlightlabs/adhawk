from django.template import Context
from django.shortcuts import render_to_response

def about(request):
    return render_to_response('whopaid/about.html')
