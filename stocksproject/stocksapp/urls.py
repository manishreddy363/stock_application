from django.urls import path
from .views import stock_list, stock_analysis

urlpatterns = [
    path('stock_list/', stock_list, name='stock_list'),
    path('stock_analysis/<str:stock>/', stock_analysis, name='stock_analysis'),
]
