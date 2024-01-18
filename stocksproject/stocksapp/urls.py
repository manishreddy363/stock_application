# stocksapp/urls.py
from django.urls import path
from .views import login_view, stock_list, stock_detail

urlpatterns = [
    path('login/', login_view, name='login'),
    # path('hello_world/', hello_world, name='hello_world'),
    path('stock_list/', stock_list, name='stock_list'),
    path('stock-detail/<str:stock>/', stock_detail, name='stock_detail'),
]
