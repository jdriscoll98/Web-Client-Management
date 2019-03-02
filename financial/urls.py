from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'financial'

urlpatterns = [
		# costs views
		url(r'^add-cost/(?P<pk>\d+)/(?P<type>\w+)/$', AddCost.as_view(), name='add'),
		url(r'^remove-cost/(?P<pk>\d+)/$', DeleteCost.as_view(), name='delete'),
		url(r'^update-cost/(?P<pk>\d+)/$', UpdateCost.as_view(), name='update'),
]
