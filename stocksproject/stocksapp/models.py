from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    # Add any additional fields you need
    pass


class Stock_ID(models.Model):
    stock_name = models.CharField(max_length=30,unique=True)
    stock_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.stock_name)


class Stock_Details_Table(models.Model):
    Stock_Details_Symbol = models.CharField(max_length=30)
    Stock_Details_Name = models.CharField(max_length=30)
    Stock_Details_Description = models.TextField(max_length=250)
    Stock_Details_Country = models.CharField(max_length=30)
    Stock_Details_State = models.CharField(max_length=30)
    Stock_Details_StockID = models.ForeignKey(Stock_ID, on_delete=models.CASCADE,to_field='stock_id')
    Stock_Details_Sector = models.CharField(max_length=30)
    Stock_Details_Industry = models.CharField(max_length=30)
    Stock_Details_Total_Revenue = models.CharField(max_length=30)
    Stock_Details_NAICS_Code = models.IntegerField()

    def __str__(self):
        return str(self.Stock_Details_Name)


class Stock_Naics_Table(models.Model):
    Stock_Naics_Column1 = models.CharField(max_length=30)
    Stock_Naics_Level = models.IntegerField()
    Stock_Naics_Hierarchical_structure = models.CharField(max_length=30)
    Stock_Naics_Code = models.IntegerField()
    Stock_Naics_Parent = models.IntegerField(blank=True)
    Stock_Naics_Class_title = models.TextField(max_length=250,blank=True)
    Stock_Naics_Superscript = models.CharField(max_length=30,blank=True)
    Stock_Naics_Class_definition = models.TextField(max_length=250,blank=True)
    Stock_Naics_symbol = models.CharField(max_length=30,blank=True)
    Stock_Naics_StockID = models.ForeignKey(Stock_ID, on_delete=models.CASCADE,to_field='stock_id')

    def __str__(self):
        return str(self.Stock_Naics_Level)


class stock_historical_data_v3(models.Model):
    Stock_Historical_Data_V3_Column1 = models.IntegerField()
    Stock_Historical_Data_V3_Year = models.IntegerField()
    Stock_Historical_Data_V3_Quarter = models.IntegerField(blank=True,default=11)
    Stock_Historical_Data_V3_StockID = models.ForeignKey(Stock_ID, on_delete=models.CASCADE,to_field='stock_id')
    Stock_Historical_Data_V3_FilingDate = models.CharField(max_length=30)
    Stock_Historical_Data_V3_FiscalQuarterEnd = models.CharField(max_length=30)
    Stock_Historical_Data_V3_FQE_10 = models.CharField(max_length=30)
    Stock_Historical_Data_V3_Price_Next_Day = models.FloatField()
    Stock_Historical_Data_V3_Previous_Price = models.FloatField()
    Stock_Historical_Data_V3_Impact = models.FloatField()
    Stock_Historical_Data_V3_Impact_2 = models.FloatField()

    def __str__(self):
        return str(self.Stock_Historical_Data_V3_StockID)


class stock_Earnings_4(models.Model):

    Stock_Earnings_4_Estimated_EPS = models.FloatField()
    Stock_Earnings_4_Actual_EPS = models.FloatField()
    Stock_Earnings_4_StockID =  models.ForeignKey(Stock_ID, on_delete=models.CASCADE,to_field='stock_id')
    Stock_Earnings_4_EPS_Estimate_isNull = models.IntegerField()
    Stock_Earnings_4_Reported_EPS_isNull = models.IntegerField()
    Stock_Earnings_4_Surprise = models.FloatField(default=None,blank=True)
    Stock_Earnings_4_Year = models.IntegerField(default=None)
    Stock_Earnings_4_Fiscal_Quarter_End = models.CharField(max_length=30,default=None)
    Stock_Earnings_4_EI_EPS = models.FloatField()
    Stock_Earnings_4_F_Delta = models.FloatField()
    Stock_Earnings_4_EI_Delta = models.FloatField()
    Stock_Earnings_4_Date = models.CharField(max_length=30)
    Stock_Earnings_4_Quarter = models.CharField(max_length=30)
    Stock_Earnings_4_Filing_Date = models.CharField(max_length=30,default=None)
    Stock_Earnings_4_Filing_Date_2 = models.CharField(max_length=30,default=None)
    Stock_Earnings_4_Fiscal_Quarter_End_2 = models.CharField(max_length=30,default=None)
    Stock_Earnings_4_F_Delta_2 = models.FloatField(default=None)
    Stock_Earnings_4_EI_Delta_2 = models.FloatField(default=None)
    Stock_Earnings_4_EI_EPS_2 = models.FloatField(default=None)

    def __str__(self):
        return str(self.Stock_Earnings_4_StockID)


class Next_filing_dates(models.Model):
    Next_Filing_Dates_Column1 = models.IntegerField()
    Next_Filing_Dates_StockID =  models.ForeignKey(Stock_ID, on_delete=models.CASCADE,to_field='stock_id')
    Next_Filing_Dates_Avg_Diff = models.IntegerField()
    Next_Filing_Dates_DateDifference = models.IntegerField()
    Next_Filing_Dates_FiscalQuarter = models.IntegerField()

    Next_Filing_Dates_FiscalQuarterEnd = models.CharField(max_length=30)
    Next_Filing_Dates_Next_FD = models.CharField(max_length=30)

    Next_Filing_Dates_Remaining_Days = models.IntegerField()
    Next_Filing_Dates_Avg_EEPS = models.FloatField()
    Next_Filing_Dates_Avg_FEPS = models.FloatField()
    Next_Filing_Dates_Next_Actual_EPS = models.CharField(max_length=30)

    def __str__(self):
        return str(self.Next_Filing_Dates_StockID)
