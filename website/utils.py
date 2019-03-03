from financial.models import Cost


def get_profit(type):
    return sum((cost.client_payment - cost.price) for cost in Cost.objects.filter(type=type))

def get_total():
    total = 0
    for cost in Cost.objects.all():
        total += (cost.client_payment - cost.price )
    return total
