from django.urls import path
from django.http import HttpResponse

# Minimal example view
def index(request):
    return HttpResponse("Welcome to Diary!")

urlpatterns = [
    path('', index, name='index'),
]
