from django.db import models

class Client(models.Model):
    client = models.CharField(max_length=100)

    def __str__(self):
        return str(self.client)

class Cost(models.Model):
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


    client = models.ForgeinKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, chocies=TYPE_CHOICES)
    price = models.PositiveIntegerField()
    client_payment = models.IntegerField()
    first_paymnet = models.DateTimeField()
    payment_period = models.CharField(max_length=2, choices=PAYMENT_PEROID)

    def _str__(self):
        return str(self.client) + str(self.type)
