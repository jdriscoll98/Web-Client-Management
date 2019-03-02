from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'management'

urlpatterns = [
    	# client viewss
		url(r'^add-client/$', AddClient.as_view(), name='add'),
		url(r'^delete-client/(?P<pk>\d+)/$', DeleteClient.as_view(), name='delete'),
		url(r'^update-client/(?P<pk>\d+)/$', UpdateClient.as_view(), name='update'),
		url(r'^detail-client/(?P<pk>\d+)/$', DetailClient.as_view(), name='detail'),
	]
