from django.shortcuts import render

def index(request):
    params = {}
    return render(request, 'main/index.html', params)

def documentation(request):
    params = {}
    return render(request, 'main/documentation.html', params)

def weare(request):
    params = {}
    return render(request, 'main/weare.html', params)

def thanks(request):
    params = {}
    return render(request, 'main/thanks.html', params)

def apps(request):
    params = {}
    return render(request, 'main/apps.html', params)
