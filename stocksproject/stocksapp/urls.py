# stocksapp/urls.py
from django.urls import path
from .views import login_view, hello_world

urlpatterns = [
    path('login/', login_view, name='login'),
    path('search_stock/', hello_world, name='hello_world'),
]
