from django.urls import path
<<<<<<< Updated upstream
from .views import stock_list, stock_analysis, stock_chart, correlation_analysis, get_data
=======
from .views import stock_list, stock_analysis, stock_chart, correlation_analysis,get_variable_list,get_correlation_values,get_eq_values,page_3_api
>>>>>>> Stashed changes

urlpatterns = [
    path('stock_list/', stock_list, name='stock_list'),
    path('stock_analysis/<str:stock>/', stock_analysis, name='stock_analysis'),
    path('stock_chart/<str:stock>/', stock_chart, name='stock_chart'),
    path('correlation_analysis/<int:stock_id>/', correlation_analysis, name='correlation_analysis'),
<<<<<<< Updated upstream
    path('get_data/<int:stock_id>/<str:selected_value>/', get_data, name='get_data'),
]
=======
    # path('variable_list/', get_variable_list, name='variable_list'),
    # path('get_correlation_values/', get_correlation_values, name='get_correlation_values'),
    path('page_3_api/', page_3_api, name='page_3_api'),
]
>>>>>>> Stashed changes
