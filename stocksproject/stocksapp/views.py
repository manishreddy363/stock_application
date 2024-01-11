# stocksapp/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def hello_world(request):
    return render(request, 'hello_world.html', {'user': request.user})
