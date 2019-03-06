from django import template

register = template.Library()

@register.simple_tag(name="get_income")
def get_total(type, company):
    try:
        income = 0
        expense = 0
        for client in Client.objects.filter(company=company):
            for cost in ClientCost.objects.filter(client=client, type=type):
                income += cost.amount
        for cost in CompanyCost.objects.filter(company=company, type=type):
            expense += cost.amount
        return (income - expense)
    except Exception as e:
        print(e)
        return 0
