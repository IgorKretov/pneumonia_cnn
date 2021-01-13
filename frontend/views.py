from django.shortcuts import render


def index(request):
    return render(request, 'frontend/index.html')

def register(request):
    return render(request, 'frontend/register.html')

def login(request):
    return render(request, 'frontend/login.html')
