from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'financial'

urlpatterns = [
		# costs views
		url(r'^add-cost/$', AddCost.as_view(), name='add'),
		url(r'^remove-cost/(?P<pk>\d+)/$', DeleteCost.as_view(), name='delete'),
		url(r'^update-cost/(?P<pk>\d+)/$', UpdateCost.as_view(), name='update'),
		url(r'^list-cost/(?P<type>\w+)/$', ListCost.as_view(), name='list'),
		url(r'^estimate-cost/$', EstimatedCostGenerator.as_view(), name='estimate'),
		url(r'^add-service/$', AddService.as_view(), name='add_service'),
		url(r'^update-service/$', UpdateService.as_view(), name='update_service'),
		url(r'^services/$', ListServices.as_view(), name='services_list'),
]
