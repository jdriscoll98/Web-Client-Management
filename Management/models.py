from django.db import models
from django.urls import reverse
from datetime import timedelta
from financial.models import Cost
from django.core.validators import RegexValidator
# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(blank=True, null=True)
    folder_link = models.URLField(blank=True, null=True)
    additional_information = models.CharField(max_length=250, blank=True, null=True)
    amount_owed = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('website:homepage_view')

    def get_cost(self, label):
        type = Cost.TYPES.get_value(label)
        if Cost.objects.filter(client=self, type=type).exists():
            cost = Cost.objects.get(client=self, type=type)
            return cost
        else:
            return None

    def get_profit(self, type):
        try:
            cost = Cost.objects.get(client=self, type=type)
        except:
            pass
        return cost.get_total_cost()

    def get_amount_owed(self):
        total = sum(cost.client_payment for cost in Cost.objects.filter(client=self))
        return total

    def get_customer_id(self):
        return self.customer_id


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    github_link = models.URLField(blank=True, null=True)
    folder_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
