from .models import Service, Cost
from management.models import Client, Project
from django.conf import settings
import stripe
import json

def create_costs(data):
    try:
        client = Client.objects.get(name=data['client'])
        project = Project.objects.get(name=data['project'])
        project_cost = 0
        for service in Service.objects.all():
            if data[str(service)]:
                project_cost += (int(data[str(service)]) * service.cost_per_hour)
        project_cost += int(data['Plugin'])
        project_cost += int(data['Theme'])
        type = Cost.TYPES.get_value('project')
        cost, created = Cost.objects.get_or_create(
            client=client,
            project=project,
            type=type,
            defaults={
            "price": 0,
            "client_payment": project_cost,
            'payment_period': 'wk'
            })
        if not created:
            cost.client_payment += project_cost
            cost.save()
        server_hosting = Cost.TYPES.get_value('server_hosting')
        domains = Cost.TYPES.get_value('domains')
        elementor = Cost.TYPES.get_value('elementor')
        cost, created = Cost.objects.get_or_create(
            client=client,
            type=server_hosting,
            defaults={
                "project": project,
                "price": 0,
                "client_payment": int(data['Server Hosting']),
                "payment_period": 'mo',
            }
        )
        if not created:
            cost.client_payment += int(data['Server Hosting'])
            cost.save()
        cost, created = Cost.objects.get_or_create(
            client=client,
            type=domains,
            defaults={
                "project": project,
                "price": 0,
                "client_payment": int(data['Domains']),
                "payment_period": 'an',
            }
        )
        if not created:
            cost.client_payment += int(data['Domains'])
            cost.save()
        cost, created = Cost.objects.get_or_create(
            client=client,
            type=elementor,
            defaults={
                "project": project,
                "price": 0,
                "client_payment": int(data['Elementor']),
                "payment_period": 'an',
            }
        )
        if not created:
            cost.client_payment += int(data['Elementor'])
            cost.save()
        return True
    except Exception as e:
        print(e)
        return False

def create_customer(client):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = stripe.Customer.create(
            description = "customer for %s" % (str(client)),
            email = client.email
        )
        return customer, True
    except Exception as e:
        print(e)
        return "", False

def send_invoice(customer_id, amount, description, due_date):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        stripe.InvoiceItem.create(
            customer=customer_id,
            amount=amount * 100,
            currency="usd",
            description=description,
        )
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

def get_invoices():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    invoice_list = []
    invoices = stripe.Invoice.list(limit=100)['data']
    return invoices
