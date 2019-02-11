from .models import Cost


def get_total_profit():
    profits = {}
    total = 0
    for x in Cost.TYPES:
        type = x.value[0]
        profits[type] = 0
        for profit in Cost.objects.filter(type=type):
            profits[type] += profit.get_profit()
            total += profit.get_profit()
    return profits, total

def get_type_profit(type):
    profits = 0
    for profit in Cost.objects.fitler(type=type):
        profits += profit.get_profit()
    return profit
