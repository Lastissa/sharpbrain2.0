from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect



from datetime import datetime as dt

from django.urls import reverse

# Create your views here.
def active(self):
    return JsonResponse(
        {
        'name' : 'ope',
        'date' : dt.now(),
    }
        )

def json_1(self):
    return JsonResponse({
        'Name' : 'Opeyemi',
    })
    
    
