from django.contrib import admin
from .models import ClientCost, CompanyCost, Service
# Register your models here.
admin.site.register(ClientCost)
admin.site.register(CompanyCost)
admin.site.register(Service)
