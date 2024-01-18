from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Stock_ID


@login_required(login_url='/')
def stock_list(request):

    stock_list_queryset = Stock_ID.objects.all().values()
    stock_list_object = list(stock_list_queryset)
    stocks= []
    for stock in stock_list_object:
        stocks.append(stock['stock_name']) 

    # Get the search query from the request
    query = request.GET.get('search', '')

    # Filter stocks based on the search query
    matching_stock_list = [stock for stock in stocks if stock.lower().startswith(query.lower())]
    matching_stock_list.sort()

    return render(request, 'stock_list.html', {'stocks': matching_stock_list, 'query': query})


def stock_analysis(request, stock):
    # Retrieve stock details based on the stock symbol
    # (You need to implement this view)
    # For example, you might query a database for the details of the selected stock.
    # stock_details = get_stock_details(stock)
    
    # Render the stock detail page with the details
    return render(request, 'stock_detail_analysis.html', {'stock': stock})
