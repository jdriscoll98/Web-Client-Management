from .models import Service, ClientCost, Cost
from management.models import Client, Project, Company
import stripe
import json
from datetime import datetime

def create_costs(data):
    try:
        company = Company.objects.get(pk=data['company'])
        key = company.stripe_secret
        client = Client.objects.get(name=data['client'])
        project = Project.objects.get(name=data['project'])
        datetime_object = datetime.strptime(data['due_date'], '%Y-%m-%d')
        due_date =  int(datetime_object.timestamp())
        project_cost = 0
        for service in Service.objects.all():
            if data[str(service)]:
                project_cost += (int(data[str(service)]) * service.cost_per_hour)
        create_invoice_item(key, client, int(project_cost), str(project))
        for type in CostType.objects.filter(company=company):
            cost, created = ClientCost.objects.get_or_create(
                client=client,
                type=type,
                defaults={
                    "project": project,
                    "amount": int(data[str(type)]),
                    "payment_period": type.payment_period,
                }
            )
            if not created:
                cost.amount += int(data[str(type)])
                cost.save()
            create_invoice_item(key, client, int(cost.amount), str(type))
        send_invoice(key, client, due_date)
        return True
    except Exception as e:
        print(e)
        return False

def send_invoice(key, client, due_date):
    stripe.api_key = key
    try:
        customer_id = client.customer_id
        invoice = stripe.Invoice.create(
            customer=customer_id,
            billing='send_invoice',
            due_date = due_date,
        )
        invoice.send_invoice()
        return True
    except Exception as e:
        print(e)
        return False

def create_invoice_item(key, client,  amount, description):
    stripe.api_key = key
    try:
        if not client.customer_id:
            customer = stripe.Customer.create(
                description = "customer for %s" % (str(client)),
                email = client.email
            )
            client.customer_id = customer['id']
            client.save()
        customer_id = client.customer_id
        stripe.InvoiceItem.create(
            customer=customer_id,
            amount=amount * 100,
            currency="usd",
            description=description,
        )
        return True
    except Exception as e:
        print(e)
        return False

def get_invoices(key):
    stripe.api_key = key
    invoice_list = []
    invoices = stripe.Invoice.list(limit=100)['data']
    return invoices

def get_invoice_items(id, key):
    try:
        stripe.api_key = key
        invoice_items = stripe.InvoiceItem.list(limit=100, invoice=id)
    except Exception as e:
        print(e)
        invoice_items = []

    return invoice_items


def get_client_costs(company, type):
    costs = []
    for client in Client.objects.filter(company=company):
        for cost in ClientCost.objects.filter(client=client, type=type):
            costs.append(cost)
    return costs
