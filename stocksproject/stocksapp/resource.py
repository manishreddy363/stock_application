from import_export import resources,fields
from .models import *
from import_export.widgets import ForeignKeyWidget


class Stock_Details_Resource(resources.ModelResource):
    Stock_Details_StockID = fields.Field(
        column_name = 'Stock_Details_StockID',
        attribute = 'Stock_Details_StockID',
        widget=ForeignKeyWidget(Stock_ID,'stock_id')
    )
    class Meta:
        model = Stock_Details_Table

class Stock_Naics_Resource(resources.ModelResource):
    Stock_Naics_StockID = fields.Field(
        column_name = 'Stock_Naics_StockID',
        attribute = 'Stock_Naics_StockID',
        widget=ForeignKeyWidget(Stock_ID,'stock_id')
    )
    class Meta:
        model = Stock_Naics_Table

class stock_historical_data_v3_Resource(resources.ModelResource):
    Stock_Historical_Data_V3_StockID = fields.Field(
        column_name = 'Stock_Historical_Data_V3_StockID',
        attribute = 'Stock_Historical_Data_V3_StockID',
        widget=ForeignKeyWidget(Stock_ID,'stock_id')
    )
    class Meta:
        model = stock_historical_data_v3

class stock_Earnings_4_Resource(resources.ModelResource):
    Stock_Earnings_4_StockID = fields.Field(
        column_name = 'Stock_Earnings_4_StockID',
        attribute = 'Stock_Earnings_4_StockID',
        widget=ForeignKeyWidget(Stock_ID,'stock_id')
    )
    class Meta:
        model = stock_Earnings_4

class Next_filing_dates_Resource(resources.ModelResource):
    Next_Filing_Dates_StockID = fields.Field(
        column_name = 'Next_Filing_Dates_StockID',
        attribute = 'Next_Filing_Dates_StockID',
        widget=ForeignKeyWidget(Stock_ID,'stock_id')
    )
    class Meta:
        model = Next_filing_dates