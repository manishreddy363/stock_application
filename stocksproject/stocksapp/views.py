from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock_ID, Stock_Details_Table,Stock_Naics_Table,stock_historical_data_v3,Next_filing_dates, Variable_table, Correlation_values,EQ_Table
from .models import stock_Earnings_4 as stock_Earnings
from .forms import StockForm
import pandas as pd
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from io import BytesIO
import base64
<<<<<<< Updated upstream
# import random
from matplotlib.ticker import FuncFormatter
from django.http import JsonResponse
import matplotlib
=======
from .resource import EQ_Table_Resource
>>>>>>> Stashed changes

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
            # 'stock_price':random.randint(1,5),
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

        
        data1 = stock_earnings_list
        x_axis_1 = list(stock_earnings_dict.keys())[:2]
        y_axis_1 = list(stock_earnings_dict.keys())[2:]
        colors1 = ['blue', 'green', 'red', 'purple', 'orange']
        legend_position1 = (0.81, 1)
        bars1 = 3

        data2 = stock_historical_list
        x_axis_2 = list(item_historical_dict.keys())[:2]
        y_axis_2 = list(item_historical_dict.keys())[2:]
        colors2 = ['blue', 'green', 'red']
        legend_position2 = (0.58, 1)
        bars2 = 2

        chart_url_1 = stock_chart(x_axis_1, y_axis_1, data1, colors1, bars1, legend_position1)
        chart_url_2 = stock_chart(x_axis_2, y_axis_2, data2, colors2, bars2, legend_position2)

        return render(request, 'stock_detail_analysis.html', {'stock_analysis_data': stock_analysis_data,
                                                              'eps_data': stock_earnings_list,
                                                              'stock_revenue': stock_revenue_dict,
                                                              'stock_naics_code': stock_analysis_data['naics_code'],
                                                              'fiscal_data': stock_historical_list,
                                                              'next_period_data':next_filing_list,
                                                              'form': form, 'error_message': error_message,
                                                              'stock_input':stock, 'chart_url_1': chart_url_1,
                                                              'chart_url_2': chart_url_2})
    except Exception as e:
        print("invalid stock id")
        print(f"Exception: {e}")
        messages.error(request, 'Invalid {} stock name'.format(stock))


def stock_chart(xaxis, yaxis, data, colors, bars, legend_position, format_y_axis=False):

    selected_y_axis = yaxis
    # Set the Matplotlib backend explicitly
    matplotlib.use('Agg')

    # Generate chart if the form is submitted
    df = pd.DataFrame(data)
    x_column = xaxis[0]
    # Adjust the size of the entire graph
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_facecolor('lightgray')
    fig.patch.set_facecolor('lightgray')
    # Display x-axis values vertically
    ax.set_xticklabels(df[x_column], rotation=90, ha='center', fontsize=6)
    ax.tick_params(axis='y', labelsize=6)
    bar_width = 0.2
    x_positions = len(df[x_column])
    for i, (y_column, color) in enumerate(zip(selected_y_axis, colors)):
        if i < bars:
            ax.bar([pos + i * bar_width for pos in range(x_positions)], df[y_column], label=y_column, alpha=0.7, width=bar_width, color=color)
        else:
            ax.plot(df[x_column], df[y_column], label=y_column, color=color)

    # Applying the formatter to the y-axis
    if format_y_axis:
        ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    # ax.set_xlabel('X Axis')
    # ax.set_ylabel('Y Axis')
    # Set the y-axis step to be +1 or -1 or integer
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    legend_labels = yaxis
    legend = ax.legend(loc='lower right', bbox_to_anchor=(1, 1), ncol=len(legend_labels), fancybox=True, fontsize='small', labels=legend_labels)
    legend.set_bbox_to_anchor(legend_position)

    # Adjust the spacing around the subplots to make the table occupy all available space
    plt.subplots_adjust(right=1, left=0.05, top=0.9, bottom=0.18)

    img = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return chart_url


@login_required(login_url='/')
def correlation_analysis(request, stock_id):
    print(stock_id)
    correlation_data = 'correlation_data'
    correlation_data = [{'Period':'30-Dec-23', 'Value':37742, 'Blank':4656926},
                        {'Period':'31-Dec-23', 'Value':77482, 'Blank':4774824},
                        {'Period':'32-Dec-23', 'Value':67742, 'Blank':6774826},
                        {'Period':'33-Dec-23', 'Value':47762, 'Blank':4677482},
                        {'Period':'34-Dec-23', 'Value':35742, 'Blank':6377482},
                        {'Period':'35-Dec-23', 'Value':94742, 'Blank':3377482},
                        {'Period':'36-Dec-23', 'Value':74742, 'Blank':3377482},
                        {'Period':'37-Dec-23', 'Value':64742, 'Blank':2377482},
                        {'Period':'38-Dec-23', 'Value':84742, 'Blank':5377482},
                        {'Period':'39-Dec-23', 'Value':44742, 'Blank':7377482},
                        {'Period':'40-Dec-23', 'Value':24742, 'Blank':9377482},
                        {'Period':'41-Dec-23', 'Value':44742, 'Blank':7377482},
                        {'Period':'42-Dec-23', 'Value':64742, 'Blank':6377482},
                        {'Period':'43-Dec-23', 'Value':44742, 'Blank':4377482},
                        {'Period':'44-Dec-23', 'Value':54742, 'Blank':8377482},
                        {'Period':'45-Dec-23', 'Value':44742, 'Blank':2377482},
                        {'Period':'46-Dec-23', 'Value':84742, 'Blank':2477482},]
    try:
        stock_name = Stock_ID.objects.get(stock_id=stock_id).stock_name
        stock_data = Stock_Details_Table.objects.get(Stock_Details_StockID=stock_id)
        print(stock_data)
        data = correlation_data
        x_axis = list(correlation_data[0].keys())[:1]
        y_axis = list(correlation_data[0].keys())[1:]
        colors = ['blue', 'green']
        legend_position = (0.58, 1)
        bars = 0

        chart_url = stock_chart(x_axis, y_axis, data, colors, bars, legend_position, format_y_axis=True)
        return render(request, 'correlation_analysis.html', {'correlation_data': correlation_data,
                                                             'chart_url': chart_url, 'stock_id': stock_id})
    except Exception as e:
        print("invalid stock id")
        print(f"Exception: {e}")
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

<<<<<<< Updated upstream
def millions_formatter(x, pos):
    return f"${x / 1e6:.1f}M"



def get_data(request, stock_id, selected_value):

    print(stock_id)
    if selected_value == '1':
        table_data = [{'Period':'30-Dec-23', 'Value':37742, 'Blank':4656926},
                        {'Period':'31-Dec-23', 'Value':77482, 'Blank':4774824},
                        {'Period':'32-Dec-23', 'Value':67742, 'Blank':6774826},
                        {'Period':'33-Dec-23', 'Value':47762, 'Blank':4677482},
                        {'Period':'34-Dec-23', 'Value':35742, 'Blank':6377482},
                        {'Period':'35-Dec-23', 'Value':94742, 'Blank':3377482},
                        {'Period':'36-Dec-23', 'Value':74742, 'Blank':3377482},
                        {'Period':'37-Dec-23', 'Value':64742, 'Blank':2377482},
                        {'Period':'38-Dec-23', 'Value':84742, 'Blank':5377482},
                        {'Period':'39-Dec-23', 'Value':44742, 'Blank':7377482},
                        {'Period':'40-Dec-23', 'Value':24742, 'Blank':9377482},
                        {'Period':'41-Dec-23', 'Value':44742, 'Blank':7377482},
                        {'Period':'42-Dec-23', 'Value':64742, 'Blank':6377482},
                        {'Period':'43-Dec-23', 'Value':44742, 'Blank':4377482},
                        {'Period':'44-Dec-23', 'Value':54742, 'Blank':8377482},
                        {'Period':'45-Dec-23', 'Value':44742, 'Blank':2377482},
                        {'Period':'46-Dec-23', 'Value':84742, 'Blank':2477482},]
    else:
        table_data = [{'Period':'30-Dec-23', 'Value':27742, 'Blank':4656926},
                        {'Period':'31-Dec-23', 'Value':57482, 'Blank':4774824},
                        {'Period':'32-Dec-23', 'Value':37742, 'Blank':6774826},
                        {'Period':'33-Dec-23', 'Value':67762, 'Blank':4677482},
                        {'Period':'34-Dec-23', 'Value':95742, 'Blank':6377482},
                        {'Period':'35-Dec-23', 'Value':24742, 'Blank':3377482},
                        {'Period':'36-Dec-23', 'Value':44742, 'Blank':3377482},
                        {'Period':'37-Dec-23', 'Value':24742, 'Blank':2377482},
                        {'Period':'38-Dec-23', 'Value':34742, 'Blank':5377482},
                        {'Period':'39-Dec-23', 'Value':64742, 'Blank':7377482},
                        {'Period':'40-Dec-23', 'Value':74742, 'Blank':9377482},
                        {'Period':'41-Dec-23', 'Value':34742, 'Blank':7377482},
                        {'Period':'42-Dec-23', 'Value':84742, 'Blank':6377482},
                        {'Period':'43-Dec-23', 'Value':84742, 'Blank':4377482},
                        {'Period':'44-Dec-23', 'Value':34742, 'Blank':8377482},
                        {'Period':'45-Dec-23', 'Value':54742, 'Blank':2377482},
                        {'Period':'46-Dec-23', 'Value':44742, 'Blank':2477482},]
    # stock_name = Stock_ID.objects.get(stock_id=stock_id).stock_name
    # stock_data = Stock_Details_Table.objects.get(Stock_Details_StockID=stock_id)
    # print(stock_data)
    data = table_data
    x_axis = list(table_data[0].keys())[:1]
    y_axis = list(table_data[0].keys())[1:]
    graph_data_y1 = []
    graph_data_y2 = []
    for row in table_data:
        graph_data_y1.append(row['Value'])
        graph_data_y2.append(row['Blank'])
    colors = ['blue', 'green']
    legend_position = (0.58, 1)
    bars = 0

    chart_url = stock_chart(x_axis, y_axis, data, colors, bars, legend_position, format_y_axis=True)

    data = {'table_data': table_data, 'graph_data_y1': graph_data_y1, 'graph_data_y2': graph_data_y2,
            'chart_url': chart_url}

    return JsonResponse(data)

=======

def get_variable_list():

    variable_list_queryset = Variable_table.objects.all().values_list('Variables_VariableID','Variables_VariableName')
    variable_list_object_1 = list(variable_list_queryset)
    var_list = []
    for item in variable_list_object_1:
        var_dict = {"variable_id":item[0],"variable_name":item[1]}
        var_list.append(var_dict)
    # return variable_list_object
    # variable_list_object_2 = Variable_table.objects.all().values_list('Variables_VariableID', 'Variables_VariableName')
    # return render(request, '3_page.html', {'variable_list': variable_list_object_1,'variable_list_object_2':variable_list_object_2})
    return var_list


def get_correlation_values(stock,variable_id):
    try:
        variable_name = Variable_table.objects.get(Variables_VariableID=int(variable_id)).Variables_VariableShort
    except:
        print("invalid variable id")
        messages.error(request, 'Invalid {} variable Id'.format(variable_id))

    try:
        stock_id = Stock_ID.objects.get(stock_name=stock).stock_id
    except:
        print("invalid stock id")
        messages.error(request, 'Invalid {} stock Id'.format(stock_name))

    correlation_values_list_queryset = Correlation_values.objects.filter(T3_Index__icontains=variable_name,Correlation_stock_id=stock_id).all().values()
    correlation_values_list = list(correlation_values_list_queryset)

    return correlation_values_list

    # return render(request, '3_page.html', {'variable_list': correlation_values_list})

def get_eq_values(stock,index):
    # try:
    #     variable_name = Correlation_values.objects.get(T3_Index=int(variable_id)).Variables_VariableShort
    # except:
    #     print("invalid variable id")
    #     messages.error(request, 'Invalid {} variable Id'.format(variable_id))

    eq_list_queryset = EQ_Table.objects.filter(Index=index,Symbol=stock).values()
    eq_values_list = list(eq_list_queryset)
    return eq_values_list
    # return render(request, '3_page.html', {'variable_list': eq_values_list})


def page_3_api(request,stock='DOL.TO',variable=None,index=None):
    """
    "page_3": {
    # allways get all
    "variable_list": [ {"id":1,"name":"variable_name"}, {"id":1,"name":"variable_name"} ],

    # filter based on selected variable & stock ( by default 1st variable selected for any stock)
    "correlation_list": [{"index":"","correlation_Coefficient":""},{"index":"","correlation_Coefficient":""}]

    # filter based on selected correlation & stock ( by default 1st correlation selected for any stock)
    "eq_list": [{"Period":"","Value":"","StockValue":"","Quarters":""},{"Period":"","Value":"","StockValue":"","Quarters":""}]
    }
    """

    var_list = get_variable_list()

    if variable is not None:
        select_var_id = variable
    else:
        select_var_id = var_list[0]['variable_id']

    cor_list = get_correlation_values(stock,select_var_id)

    if index is not None:
        select_index = index
    else:
        select_index = cor_list[0]['T3_Index']

    eq_list = get_eq_values(stock,select_index)

    return render(request, '3_page.html', {"data":{'variable_list': var_list,
                                           'correlation_list':cor_list,
                                           'eq_list':eq_list}})
>>>>>>> Stashed changes
