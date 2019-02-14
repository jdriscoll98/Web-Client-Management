from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'management'

urlpatterns = [
    	# client viewss
		url(r'^add-client/$', AddClient.as_view(), name='add_client'),
		url(r'^delete-client/(?P<pk>\d+)/$', DeleteClient.as_view(), name='delete_client'),
		url(r'^update-client/(?P<pk>\d+)/$', UpdateClient.as_view(), name='update_client'),
		url(r'^detail-client/(?P<pk>\d+)/$', DetailClient.as_view(), name='client_detail'),
		# costs views
		url(r'^add-cost/(?P<pk>\d+)/(?P<type>\w+)/$', AddCost.as_view(), name='add_cost'),
		url(r'^remove-cost/(?P<pk>\d+)/$', DeleteCost.as_view(), name='remove_cost'),
		url(r'^update-cost/(?P<pk>\d+)/$', UpdateCost.as_view(), name='update_cost'),
		url(r'^cost-view/(?P<type>\w+)/$', CostsView.as_view(), name='view_costs'),
]
