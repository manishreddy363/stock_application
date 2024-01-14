# stocksapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages


# @login_required(login_url='/admin/login/')
def hello_world(request):
    return render(request, 'hello_world.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('hello_world')  # Replace 'home' with the name of your home view
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
