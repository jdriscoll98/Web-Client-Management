from django.db import models
from django.urls import reverse
from enum import Enum
from datetime import timedelta
from .managers import TypeManager
# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100, unique="True")
    cost_per_hour = models.DecimalField(max_digits=6, decimal_places=2)

class Cost(models.Model):
    #choices style from Two scoops of Django 1.11 best practice
    #lets you loop through choices easily
    class TYPES(Enum):
        elementor =  ('el', 'Elementor')
        server_hosting =  ('sh', 'Server Hosting')
        domains = ('do', 'Domains')
        gsuite = ('gs', 'GSuite')
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

        @classmethod
        def get_label(cls, member):
            return cls[member].value[1]

    #using model managers to index data
    objects = models.Manager()
    TypeManager = TypeManager()


    #another way to do choices
    BIWEEKLY = 'wk'
    MONTHLY = 'mo'
    ANNUALY = 'an'

    PAYMENT_PEROID = (
        (BIWEEKLY, 'Bi-weekly'),
        (MONTHLY, 'Monthly'),
        (ANNUALY, 'Annualy')
    )


    client = models.ForeignKey('management.Client', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=[x.value for x in TYPES])
    price = models.PositiveIntegerField()
    client_payment = models.IntegerField()
    last_payment_date = models.DateTimeField()
    payment_period = models.CharField(max_length=2, choices=PAYMENT_PEROID, default=BIWEEKLY)


    def __str__(self):
        return str(self.client) + ' | ' + str(self.type)

    def get_absolute_url(self):
        #returns to the clients page after adding/updating a cost
        return reverse()

    def get_profit(self):
        return  int(self.client_payment) - int(self.price)

    def get_next_payment(self):
        if self.payment_period == self.BIWEEKLY:
            next_payment = self.last_payment_date + timedelta(days=14)
        elif self.payment_period == self.MONTHLY:
            next_payment = self.last_payment_date + timedelta(weeks=4)
        else:
            next_payment = self.last_payment_date + timedelta(weeks=52)
        return next_payment
