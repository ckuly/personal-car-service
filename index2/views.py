from django.http import HttpResponse
from django.shortcuts import render

def index2(request):
    return HttpResponse("Labas, vakaras!")