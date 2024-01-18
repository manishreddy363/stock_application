# stocksapp/urls.py
from django.urls import path
from .views import login_view, hello_world, stock_search, stock_detail

urlpatterns = [
    path('login/', login_view, name='login'),
    path('search_stock/', hello_world, name='hello_world'),
    path('stock_search/', stock_search, name='stock_search'),
    path('stock-detail/<str:stock>/', stock_detail, name='stock_detail'),
]
