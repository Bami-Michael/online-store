from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache




@never_cache 
def home(request):
    return render(request, 'index.html', {} )