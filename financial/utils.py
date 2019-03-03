from .models import Service, Cost
from management.models import Client, Project

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
