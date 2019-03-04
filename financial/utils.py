from .models import Service, ClientCost, Cost
from management.models import Client, Project
from django.conf import settings
import stripe
import json
from datetime import datetime

def create_costs(data):
    try:
        client = Client.objects.get(name=data['client'])
        project = Project.objects.get(name=data['project'])
        datetime_object = datetime.strptime(data['due_date'], '%Y-%m-%d')
        due_date =  int(datetime_object.timestamp())
        project_cost = 0
        for service in Service.objects.all():
            if data[str(service)]:
                project_cost += (int(data[str(service)]) * service.cost_per_hour)
        project_cost += int(data['Plugin'])
        project_cost += int(data['Theme'])
        type = Cost.TYPES.get_value('project')
        cost, created = ClientCost.objects.get_or_create(
            client=client,
            project=project,
            type=type,
            defaults={
            "amount": project_cost,
            'payment_period': 'wk'
            })
        if not created:
            cost.amount += project_cost
            cost.save()
        send_invoice(client, int(project_cost), str(project), due_date)
        server_hosting = Cost.TYPES.get_value('server_hosting')
        domains = Cost.TYPES.get_value('domains')
        elementor = Cost.TYPES.get_value('elementor')
        cost, created = ClientCost.objects.get_or_create(
            client=client,
            type=server_hosting,
            defaults={
                "project": project,
                "amount": int(data['Server Hosting']),
                "payment_period": 'mo',
            }
        )
        if not created:
            cost.amount += int(data['Server Hosting'])
            cost.save()
        cost, created = ClientCost.objects.get_or_create(
            client=client,
            type=domains,
            defaults={
                "project": project,
                "amount": int(data['Domains']),
                "payment_period": 'an',
            }
        )
        if not created:
            cost.amount += int(data['Domains'])
            cost.save()
        cost, created = ClientCost.objects.get_or_create(
            client=client,
            type=elementor,
            defaults={
                "project": project,
                "amount": int(data['Elementor']),
                "payment_period": 'an',
            }
        )
        if not created:
            cost.amount += int(data['Elementor'])
            cost.save()
        return True
    except Exception as e:
        print(e)
        return False

def send_invoice(client, amount, description, due_date):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        if not client.customer_id:
            customer_id = stripe.Customer.create(
                description = "customer for %s" % (str(client)),
                email = client.email
            )
            client.customer_id = customer_id
            client.save()
        else:
            customer_id = client.customer_id
        stripe.InvoiceItem.create(
            customer=customer_id,
            amount=amount * 100,
            currency="usd",
            description=description,
        )
        print('item created')
        invoice = stripe.Invoice.create(
            customer=customer_id,
            billing='send_invoice',
            due_date = due_date,
        )
        print('invoice created')
        invoice.send_invoice()
        return True
    except Exception as e:
        print(e)
        return False

def get_invoices():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    invoice_list = []
    invoices = stripe.Invoice.list(limit=100)['data']
    return invoices

def get_client_costs(company, type):
    costs = []
    for client in Client.objects.filter(company=company):
        for cost in ClientCost.objects.filter(client=client, type=type):
            costs.append(cost)
    return costs
