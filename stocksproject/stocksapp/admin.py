from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Stock_Naics_Table,stock_Earnings_4,Stock_Details_Table,Next_filing_dates,stock_historical_data_v3,Stock_ID,Variable_table,Correlation_values,EQ_Table
from import_export.admin import ImportExportModelAdmin
from .resource import *
# Register your models here.
admin.site.register(CustomUser, UserAdmin)

class Stock_Details_Table_Admin(ImportExportModelAdmin):
    resource_class = Stock_Details_Resource

admin.site.register(Stock_Details_Table,Stock_Details_Table_Admin)

class stock_Earnings_4_Admin(ImportExportModelAdmin):
    resource_class = stock_Earnings_4_Resource

admin.site.register(stock_Earnings_4,stock_Earnings_4_Admin)

class Stock_Naics_Admin(ImportExportModelAdmin):
    resource_class = Stock_Naics_Resource

admin.site.register(Stock_Naics_Table,Stock_Naics_Admin)

class Next_filing_dates_Admin(ImportExportModelAdmin):
    resource_class = Next_filing_dates_Resource

admin.site.register(Next_filing_dates,Next_filing_dates_Admin)

class stock_historical_data_v3_Admin(ImportExportModelAdmin):
    resource_class = stock_historical_data_v3_Resource

admin.site.register(stock_historical_data_v3,stock_historical_data_v3_Admin)

admin.site.register(Stock_ID)

class Variable_Admin(ImportExportModelAdmin):
    resource_class = Variable_table_Resource
admin.site.register(Variable_table,Variable_Admin)

class Correlation_values_Admin(ImportExportModelAdmin):
    resource_class = Correlation_values_Resource
admin.site.register(Correlation_values,Correlation_values_Admin)

class EQ_Table_Admin(ImportExportModelAdmin):
    resource_class = EQ_Table_Resource
admin.site.register(EQ_Table,EQ_Table_Admin)