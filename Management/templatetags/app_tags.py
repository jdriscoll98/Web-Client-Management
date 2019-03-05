from django import template

register = template.Library()
@register.simple_tag(name="get_customer")
def get_customer(customer_id):
    return str(Client.objects.get(customer_id=customer_id))
