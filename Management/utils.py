from financial.models import CompanyCost, ClientCost
from management.models import Client

def get_company_cost(company, type):
    try:
        return CompanyCost.objects.get(company=company, type=type)
    except:
        return 0

def get_total(company):
    try:
        income = 0
        expense = 0
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

def get_project_income(company):
    amount = 0
    for client in Client.objects.filter(company=company):
        amount += sum(project.amount for project in Project.objects.filter(client=client))
    return amount
