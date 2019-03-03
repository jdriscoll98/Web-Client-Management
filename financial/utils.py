from .models import Service, Cost
from management.models import Client, Project

def create_costs(data):
    try:
        client = Client.objects.get(name=data['client'])
        print(data['project'])
        project = Project.objects.get(name=data['project'])
        project_cost = 0
        for service in Service.objects.all():
            if data[str(service)]:
                project_cost += (int(data[str(service)]) * service.cost_per_hour)
        project_cost += int(data['Plugin'])
        project_cost += int(data['Theme'])
        type = Cost.TYPES.get_value('project')
        Cost.objects.create(
            client=client,
            project=project,
            type=type,
            price= 0,
            client_payment = project_cost,
            payment_period = 'wk')
        server_hosting = Cost.TYPES.get_value('server_hosting')
        domains = Cost.TYPES.get_value('domains')
        elementor = Cost.TYPES.get_value('elementor')
        Cost.objects.create(
            client=client,
            project=project,
            type=server_hosting,
            price=0,
            client_payment = int(data['Server Hosting']),
            payment_period = 'mo'
        )
        Cost.objects.create(
            client=client,
            project=project,
            type=domains,
            price=0,
            client_payment = int(data['Domains']),
            payment_period = 'mo'
        )
        Cost.objects.create(
            client=client,
            project=project,
            type=elementor,
            price=0,
            client_payment = int(data['Elementor']),
            payment_period = 'mo'
        )
        return True
    except Exception as e:
        print(e)
        return False
