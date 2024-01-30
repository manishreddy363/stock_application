from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock_ID, Stock_Details_Table,Stock_Naics_Table,stock_historical_data_v3,Next_filing_dates
from .models import stock_Earnings_4 as stock_Earnings
from .forms import StockForm
import pandas as pd
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from io import BytesIO
import base64


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
        stock_analysis_data["stock_id"] = stock_id
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

        error_message = None
        default_stock_value = stock  # Replace this with your desired default value
        if request.method == 'POST':
            form = StockForm(request.POST)
            if form.is_valid():
                stock_input = form.cleaned_data['stock_input']

                # Add your validation logic here
                # For example, check if stock_input is valid

                if is_valid_stock(stock_input):
                    # Redirect to another page with a valid input
                    return redirect('stock_analysis', stock=stock_input)
                else:
                    # Set error_message if the input is invalid
                    error_message = "Invalid stock input."

        else:
            form = StockForm(initial={'stock_input': default_stock_value})

        # return render(request, 'stock_detail_analysis.html', {'form': form, 'error_message': error_message})

        return render(request, 'stock_detail_analysis.html', {'stock_analysis_data': stock_analysis_data,
                                                              'eps_data': stock_earnings_list,
                                                              'stock_revenue': stock_revenue_dict,
                                                              'stock_naics_code': stock_analysis_data['naics_code'],
                                                              'fiscal_data': stock_historical_list,
                                                              'next_period_data':next_filing_list,
                                                              'form': form, 'error_message': error_message,
                                                              'stock_input':stock})
    except Exception as e:
        print("invalid stock id")
        print(f"Exception: {e}")
        messages.error(request, 'Invalid {} stock name'.format(stock))


def stock_chart(request, stock):
    print(stock)
    stock_id = Stock_ID.objects.get(stock_name=stock).stock_id
    stock_earnings_data = stock_Earnings.objects.filter(Stock_Earnings_4_StockID
                                                            =stock_id).values()
    data = []
    for item in stock_earnings_data:
        stock_earnings_dict1 = {'filing_date':item['Stock_Earnings_4_Filing_Date_2'],
                                'forecasted_eps':item['Stock_Earnings_4_Estimated_EPS'],
                                'ei_eps':item['Stock_Earnings_4_EI_EPS_2'],
                                'actual_eps':item['Stock_Earnings_4_Actual_EPS'],
                                'f_delta':item['Stock_Earnings_4_F_Delta_2'],
                                'ei_delta':item['Stock_Earnings_4_EI_Delta_2']}
        # stock_earnings_dict2 = {'filing_date':'3-Mar-23',
        #                         'forecasted_eps':0.3,
        #                         'ei_eps':0.4,
        #                         'actual_eps':0.5,
        #                         'f_delta':0.6,
        #                         'ei_delta':0.3}
    data.append(stock_earnings_dict1)
    # data.append(stock_earnings_dict2)
    # form = YAxisSelectionForm(request.POST or None)

    # if request.method == 'POST' and form.is_valid():
    #     selected_y_axis = form.cleaned_data.get('y_axis_options', [])

    #     if not selected_y_axis:
    #         # If no y-axis options are selected, default to all columns
    selected_y_axis = ['forecasted_eps', 'ei_eps', 'actual_eps', 'f_delta', 'ei_delta']

    # Set the Matplotlib backend explicitly
    matplotlib.use('Agg')

    # Generate chart if the form is submitted
    df = pd.DataFrame(data)
    x_column = 'filing_date'

    fig, ax = plt.subplots()
    for y_column in selected_y_axis:
        ax.plot(df[x_column], df[y_column], label=y_column)

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.legend()

    img = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    return render(request, 'chart_content.html', {'chart_url': chart_url, 'stock': stock})

    # return render(request, 'table.html', {'data': data, 'form': form, 'stock': stock})


@login_required(login_url='/')
def correlation_analysis(request, stock_id):
    print(stock_id)
    correlation_data = 'correlation_data'
    try:
        stock_name = Stock_ID.objects.get(stock_id=stock_id).stock_name
        stock_data = Stock_Details_Table.objects.get(Stock_Details_StockID=stock_id)
        print(stock_data)
        return render(request, 'correlation_analysis.html', {'correlation_data': correlation_data})
    except:
        print("invalid stock id")
        messages.error(request, 'Invalid {} stock name'.format(stock_name))


def is_valid_stock(stock_input):
    stock_list_queryset = Stock_ID.objects.all().values()
    stock_list_object = list(stock_list_queryset)
    stocks= []
    for stock in stock_list_object:
        stocks.append(stock['stock_name'].lower()) 
    if stock_input.lower() in stocks:
        return True
    return False

