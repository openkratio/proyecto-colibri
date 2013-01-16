from django.shortcuts import render
from django.template import RequestContext

def index(request):
    params = {}
    return render(request, 'main/index.html', params)

def documentation(request):
    params = {}
    return render(request, 'main/documentation.html', params)

def weare(request):
    params = {}
    return render(request, 'main/weare.html', params)
