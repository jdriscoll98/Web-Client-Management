from django import template
from management.models import Client
from datetime import datetime
import pytz


register = template.Library()
@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key).value()

@register.simple_tag(name="get_customer")
def get_customer(customer_id):
    print(customer_id)
    return str(Client.objects.get(customer_id=customer_id))

@register.simple_tag(name="get_amount")
def get_amount(amount):
    return int(amount) / 100

@register.simple_tag(name="get_date")
def get_datae(timestamp):
    local_tz = pytz.timezone("US/Eastern")
    utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    date = utc_dt.strftime('%B %d, %Y')
    return date
