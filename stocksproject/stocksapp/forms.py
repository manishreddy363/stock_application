# forms.py
from django import forms

class StockForm(forms.Form):
    stock_input = forms.CharField(label=False, max_length=10)
