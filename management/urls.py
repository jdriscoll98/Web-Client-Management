from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'management'

urlpatterns = [
    	# client viewss
		url(r'^add-client/$', AddClient.as_view(), name='add_client'),
		url(r'^delete-client/$', DeleteClient.as_view(), name='delete_client'),
		url(r'^update-client/$', UpdateClient.as_view(), name='update_client'),
		# costs views
		url(r'^add-cost/$', AddCost.as_view(), name='add_cost'),
		url(r'^remove-cost/$', DeleteCost.as_view(), name='remove_cost'),
		url(r'^update-cost/$', UpdateCost.as_view(), name='update_cost'),
		url(r'^cost-view/(?P<type>\w+)/$', CostsView.as_view(), name='view_costs'),
]
