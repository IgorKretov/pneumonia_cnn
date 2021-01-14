from django.shortcuts import render


def index(request):
    return render(request, 'frontend/index.html')

def register(request):
    return render(request, 'frontend/register.html')

def login(request):
    return render(request, 'frontend/login.html')

def logout(request):
    return render(request, 'frontend/logout.html')

def archive(request):
    return render(request, 'frontend/archive/index.html')

def archive_create(request):
    return render(request, 'frontend/archive/create.html')

def archive_list(request):
    return render(request, 'frontend/archive/list.html')

def archive_images(request, id):
    return render(request, 'frontend/archive/images.html')
