from .models import Service, ClientCost, CostType
from management.models import Client, Project, Company
import stripe
import json
from datetime import datetime

def create_costs(data):
    # this method is the equivalent of processing a form
    try:
        #Setting Variables
        company = Company.objects.get(pk=data['company'])
        key = company.stripe_secret
        client = Client.objects.get(name=data['client'])
        project = Project.objects.get(name=data['project'])
        datetime_object = datetime.strptime(data['due_date'], '%Y-%m-%d')
        # stripe requires timestamp for their dates
        due_date =  int(datetime_object.timestamp())
        # Generating cost for project
        project_cost = 0
        #all services are part of the project cost
        for service in Service.objects.filter(company=company):
            if data[str(service)]:
                project_cost += (int(data[str(service)]) * service.cost_per_hour)
        project.amount += project_cost
        project.save()
        # creates an invoice item
        create_invoice_item(key, client, int(project_cost), str(project))
        # generating cost for each extra type
        for type in CostType.objects.filter(company=company):
            # check if there is already a cost for this type
            cost, created = ClientCost.objects.get_or_create(
                client=client,type=type,defaults={
                    "project": project,
                    "amount": int(data[str(type)]),
                }
            )
            # if there is a previous cost, update that cost
            if not created:
                cost.amount += int(data[str(type)])
                cost.save()
            create_invoice_item(key, client, int(cost.amount), str(type))
        #sending invoice with all invoice_items
        send_invoice(key, client, due_date)
        return True
    except Exception as e:
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
        # if new customer, create a stripe customer id
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
