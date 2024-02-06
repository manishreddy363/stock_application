from django.urls import path
from .views import stock_list, stock_analysis, stock_chart, correlation_analysis, get_data

urlpatterns = [
    path('stock_list/', stock_list, name='stock_list'),
    path('stock_analysis/<str:stock>/', stock_analysis, name='stock_analysis'),
    path('stock_chart/<str:stock>/', stock_chart, name='stock_chart'),
    path('correlation_analysis/<int:stock_id>/', correlation_analysis, name='correlation_analysis'),
    path('get_data/<int:stock_id>/<str:selected_value>/', get_data, name='get_data'),
]