from financial.models import CompanyCost, ClientCost

def get_company_cost(company, type):
    try:
        return CompanyCost.objects.get(company=company, type=type)
    except:
        return 0

def get_total(company):
    try:
        income = 0
        for client in Client.objects.filter(company=company):
            for cost in ClientCost.objects.filter(client=client):
                income += cost.amount
        return (income)
    except Exception as e:
        print(e)
        return 0

def get_income_cost(company, type):
    try:
        income = 0
        for client in Client.objects.filter(company=company):
            for cost in ClientCost.objects.filter(client=client, type=type):
                income += cost.amount
        expense = CompanyCost.objects.get(company=company, type=type)
        return (income - expense.amount)
    except Exception as e:
        print(e)
        return 0
