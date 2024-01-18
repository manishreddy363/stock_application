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
            return redirect('stock_list')  # Replace 'home' with the name of your home view
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# @login_required(login_url='/stocksapp/login/')
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
