from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Stock_Naics_Table,stock_Earnings,Stock_Details_Table,Next_filing_dates,stock_historical_data_v3,Stock_ID
# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Stock_Details_Table)
admin.site.register(stock_Earnings)
admin.site.register(Stock_Naics_Table)
admin.site.register(Next_filing_dates)
admin.site.register(stock_historical_data_v3)
admin.site.register(Stock_ID)
