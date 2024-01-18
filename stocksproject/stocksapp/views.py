# stocksapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Stock_ID
from django.http import JsonResponse, HttpResponse

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


def stock_list(request):

    stock_list_queryset = Stock_ID.objects.all().values()
    stock_list_object = list(stock_list_queryset)

    """
    stock_list_object = [{'id': 1, 'stock_name': 'ATZ.TO', 'stock_id': 0}, {'id': 2, 'stock_name': 'ACQ.TO', 'stock_id': 1}]
    """

    # Get the search query from the request
    query = request.GET.get('search', '')

    # Filter stocks based on the search query
    matching_stocks = [stock for stock in stocks if stock.lower().startswith(query.lower())]
    # matching_stocks = [stock for stock in stocks if query.lower() in stock.lower()]
    matching_stocks.sort()

    return render(request, 'stock_search.html', {'stocks': stock_list_object, 'query': query})


def stock_detail(request, stock):
    # Retrieve stock details based on the stock symbol
    # (You need to implement this view)
    # For example, you might query a database for the details of the selected stock.
    # stock_details = get_stock_details(stock)
    
    # Render the stock detail page with the details
    return render(request, 'stock_detail.html', {'stock': stock})
