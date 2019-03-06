from django.db import models
from django.urls import reverse
from enum import Enum
from datetime import timedelta
import stripe

# Create your models here.

class Service(models.Model):
    class Meta:
        unique_together = (('name', 'company'), )

    name = models.CharField(max_length=100, unique="True")
    company = models.ForeignKey('management.Company', on_delete=models.CASCADE)
    cost_per_hour = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('management:company_page', kwargs={'pk': self.company.pk})

class CostType(models.Model):
    class Meta:
        unique_together = (('name', 'company'), )

    ONE_TIME = 'ot'
    BIWEEKLY = 'wk'
    MONTHLY = 'mo'
    ANNUALY = 'an'

    PAYMENT_PEROID = (
        (ONE_TIME, 'One Time'),
        (BIWEEKLY, 'Bi-weekly'),
        (MONTHLY, 'Monthly'),
        (ANNUALY, 'Annualy')
    )

    name = models.CharField(max_length=100)
    company = models.ForeignKey('management.Company', on_delete=models.CASCADE)
    payment_period = models.CharField(max_length=2, choices=PAYMENT_PEROID, default=ONE_TIME)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('management:company_page', kwargs={'pk': self.company.pk})

class Cost(models.Model):
    class Meta:
        abstract = True

    type = models.ForeignKey(CostType, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    last_payment_date = models.DateTimeField(auto_now=True)

    def get_next_payment(self):
        if self.type.payment_period == 'wk':
            next_payment = self.last_payment_date + timedelta(days=14)
        elif self.type.payment_period == 'mo':
            next_payment = self.last_payment_date + timedelta(weeks=4)
        elif self.type.payment_period == 'an':
            next_payment = self.last_payment_date + timedelta(weeks=52)
        else:
            next_pamyent = self.last_payment_date
        return next_payment

class ClientCost(Cost):
    client = models.ForeignKey('management.Client', on_delete=models.CASCADE)
    project = models.ForeignKey('management.Project', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client) + ' | ' + self.type

class CompanyCost(Cost):
    company = models.ForeignKey('management.Company', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.company) + ' | ' + self.type

    def get_absolute_url(self):
        return reverse('management:company_page', kwargs={'pk':self.company.pk})
