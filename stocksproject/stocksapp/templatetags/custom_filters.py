from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_currency(value):
    return "${:,.0f}".format(value)


@register.filter
def custom_date_format(value):
    # Convert the input string to a datetime object
    date_obj = datetime.strptime(value, '%m/%d/%Y %H:%M')
    # Format the datetime object as desired
    return date_obj.strftime('%d-%b-%y').lstrip("0").replace(" 0", " ")