from django.shortcuts import render

from stats.models import Request
from stats.plugins import LatestRequests


def index(request):
    params = {}
    return render(request, 'main/index.html', params)

