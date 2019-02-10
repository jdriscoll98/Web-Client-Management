from django.db import models
from django.urls import reverse

# Create your models here.
class Client(models.Model):
    client = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.client)

    def get_absolute_url(self):
        return reverse('website:homepage_view')

    def get_cost(self, type):
        try:
            cost = Cost.objects.get(client=self, type=type)
        except:
            pass
        return cost.price

    def get_profit(self, type):
        try:
            cost = Cost.objects.get(client=self, type=type)
        except:
            pass
        return cost.get_total_cost()


class Cost(models.Model):
    #choices style from Two scoops of Django 1.11 best practice
    ELEMENTOR = 'el'
    SERVER_HOSTING = 'sh'
    DOMAINS = 'do'
    GSUITE = 'gs'

    BIWEEKLY = 'wk'
    MONTHLY = 'mo'
    ANNUALY = 'an'

    TYPE_CHOICES = (
        (ELEMENTOR, 'Elementor'),
        (SERVER_HOSTING, 'Server Hosting'),
        (DOMAINS, 'do'),
        (GSUITE, 'gs')
    )

    PAYMENT_PEROID = (
        (BIWEEKLY, 'Bi-weekly'),
        (MONTHLY, 'Monthly'),
        (ANNUALY, 'Annualy')
    )


    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    price = models.PositiveIntegerField()
    client_payment = models.IntegerField()
    first_paymnet = models.DateTimeField()
    payment_period = models.CharField(max_length=2, choices=PAYMENT_PEROID)

    def _str__(self):
        return str(self.client) + str(self.type)

    def get_absolute_url(self):
        #returns to the clients page after adding/updating a cost
        return reverse()

    def get_total_cost(self):
        return int(self.price) - int(self.client_payment)
