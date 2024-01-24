from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Stock_ID, Stock_Details_Table,Stock_Naics_Table,stock_historical_data_v3,Next_filing_dates
from .models import stock_Earnings_4 as stock_Earnings
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


@login_required(login_url='/')
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
        stock_revenue_dict['Revenue_TTM'] = stock_data.Stock_Details_Total_Revenue
        stock_analysis_data["stock_revenue"] = stock_revenue_dict

        #NAICS code
        stock_naics_data = Stock_Naics_Table.objects.filter(Stock_Naics_StockID=stock_id).values()
        stock_naics_list = []
        for item in stock_naics_data:
            item_dict = {'code': item['Stock_Naics_Code'], 'level': item['Stock_Naics_Level'],
                         'class_title': item['Stock_Naics_Class_title']}
            stock_naics_list.append(item_dict)
        stock_analysis_data['naics_code'] = stock_naics_list

        #stock price & impact (table & chart)
        stock_historical_data = stock_historical_data_v3.objects.filter(Stock_Historical_Data_V3_StockID
                                                                   =stock_id).values()
        stock_historical_list = []
        for item in stock_historical_data:
            item_historical_dict = {'filing_date':item['Stock_Historical_Data_V3_FilingDate'],
                                    'fiscal_quarter_end':item['Stock_Historical_Data_V3_FiscalQuarterEnd'],
                                    'stock_price':item['Stock_Historical_Data_V3_FQE_10'],
                                    'next_day_stock_price':item['Stock_Historical_Data_V3_Price_Next_Day'],
                                    'impact':item['Stock_Historical_Data_V3_Impact']}
            stock_historical_list.append(item_historical_dict)

        stock_analysis_data['fiscal_data'] = stock_historical_list

        #EPS table

        stock_earnings_data = stock_Earnings.objects.filter(Stock_Earnings_4_StockID
                                                            =stock_id).values()
        stock_earnings_list = []
        for item in stock_earnings_data:
            stock_earnings_dict = {'filing_date':item['Stock_Earnings_4_Filing_Date_2'],
                                   'fiscal_quarter_end':item['Stock_Earnings_4_Fiscal_Quarter_End_2'],
                                   'forecasted_eps':item['Stock_Earnings_4_Estimated_EPS'],
                                   'ei_eps':item['Stock_Earnings_4_EI_EPS_2'],
                                   'actual_eps':item['Stock_Earnings_4_Actual_EPS'],
                                   'f_delta':item['Stock_Earnings_4_F_Delta_2'],
                                   'ei_delta':item['Stock_Earnings_4_EI_Delta_2']}
            stock_earnings_list.append(stock_earnings_dict)

        stock_analysis_data['eps_data'] = stock_earnings_list

        #next period
        next_filing_data = Next_filing_dates.objects.filter(Next_Filing_Dates_StockID
                                                                   =stock_id).values()
        next_filing_list = []
        remaining_days = 0
        for item in next_filing_data:
            next_filing_dict = {'next_filing_date':item['Next_Filing_Dates_Next_FD'],
                                'fiscal_quarter_end':item['Next_Filing_Dates_FiscalQuarterEnd'],
                                'forecasted_eps':item['Next_Filing_Dates_Avg_FEPS'],
                                'ei_eps':item['Next_Filing_Dates_Avg_EEPS'],
                                'actual_eps':item['Next_Filing_Dates_Next_Actual_EPS']}
            remaining_days +=int(item['Next_Filing_Dates_Remaining_Days'])
            next_filing_list.append(next_filing_dict)

        stock_analysis_data['next_period'] = next_filing_list

        # Trading days remaining before next filing date
        stock_analysis_data["filing_date"] = remaining_days
        return render(request, 'stock_detail_analysis.html', {'stock_analysis_data': stock_analysis_data,
                                                              'eps_data': stock_earnings_list,
                                                              'stock_revenue': stock_revenue_dict,
                                                              'stock_naics_code': stock_analysis_data['naics_code'],
                                                              'fiscal_data': stock_historical_list,
                                                              'next_period_data':next_filing_list})
    except:
        print("invalid stock id")
        messages.error(request, 'Invalid {} stock name'.format(stock))
