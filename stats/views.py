from django.shortcuts import render

from stats.models import Request
from stats.plugins import LatestRequests


def stats(request):
    params = {}
    lr = LatestRequests()

    return lr.render()

