# stocksapp/urls.py
from django.urls import path
from .views import login_view, hello_world

urlpatterns = [
    path('login/', login_view, name='login'),
    path('hello-world/', hello_world, name='hello_world'),
]
