from financial.models import CompanyCost, ClientCost
from management.models import Client

# This should be a method of the Company model
def get_company_cost(company, type):
    try:
        return CompanyCost.objects.get(company=company, type=type)
    except:
        return 0

# Get total what?
def get_total(company):
    try:
        # Put this stuff on one line
        income, expense = 0, 0

        # This should entirely be seperated out into methods of the company model
        for client in Client.objects.filter(company=company):
            for cost in ClientCost.objects.filter(client=client):
                income += cost.amount
        expenses = CompanyCost.objects.filter(company=company)
        for cost in expenses:
            expense += cost.amount
        return (income - expense)
    except Exception as e:
        print(e)
        return 0

# Same comments as above... repeating code gives development headaches
def get_income_cost(company, type):
    try:
        income = 0
        expense = 0
        for client in Client.objects.filter(company=company):
            for cost in ClientCost.objects.filter(client=client, type=type):
                income += cost.amount
        expenses = CompanyCost.objects.filter(company=company, type=type)
        for cost in expenses:
            expense += cost.amount
        return (income - expense)
    except Exception as e:
        print(e)
        return 0
