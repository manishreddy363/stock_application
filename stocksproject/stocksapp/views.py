from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Stock_ID, Stock_Details_Table
from django.http import JsonResponse, HttpResponse

# @login_required(login_url='/admin/login/')
def hello_world(request):
    return render(request, 'hello_world.html', {'user': request.user})


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
    """
    stock_analysis_data = {
    "stock_id_name":"ACP.to"
    "stock_name":"",
    "stock_description":"",
    "stock_revenue":{"county":"","provins":"","revenue":29984},
    "naics_code":[{},{},{}],
    "fiscal_data":[{},{},{}],
    "eps_data":[{},{},{}],
    "next_period":[{},{},{}],
    "filing_date":""
    }
    """
    print(stock)
    stock_analysis_data ={}
    # revenue by geography
    try:
        stock_id = Stock_ID.objects.get(stock_name=stock).stock_id
        stock_data = Stock_Details_Table.objects.get(Stock_Details_StockID=stock_id)
        print(stock_data)
        stock_analysis_data["stock_id_name"] = stock
        stock_analysis_data["stock_name"] = stock_data.Stock_Details_Name
        stock_analysis_data["description"] = stock_data.Stock_Details_Description
        stock_revenue_dict = {}
        stock_revenue_dict['Country'] = stock_data.Stock_Details_Country
        stock_revenue_dict['Province'] = stock_data.Stock_Details_State
        stock_revenue_dict['Revenue(TTM)'] = stock_data.Stock_Details_Total_Revenue

        stock_analysis_data["stock_revenue"] = stock_revenue_dict
    except:
        print("invalid stock id")
        messages.error(request, 'Invalid {} stock name'.formate(stock))

    #NAICS code
    stock_analysis_data['naics_code'] = [{'code':'',"level":"","class_title":""}]

    #stock price & impact (table & chart)
    stock_analysis_data['fiscal_data'] = [{'filing_date':'','fiscal_quarter_end':'','stock_price':'','next_day_stock_price':'','impact':''}]

    #EPS table
    stock_analysis_data['eps_data'] = [{'filing_date':'','fiscal_quarter_end':'','forecasted_eps':'',
                                        'ei_eps':'', 'actual_eps':'','f_delta':'','ei_delta':''}]

    #next period
    stock_analysis_data['next_period'] = [{'next_filing_date':'','fiscal_quarter_end':'','forecasted_eps':'',
                                        'ei_eps':'', 'actual_eps':''}]

    # Trading days remaining before next filing date
    stock_analysis_data["filing_date"] = 230

    return render(request, 'stock_detail_analysis.html', {'stock_analysis_data': stock_analysis_data})
