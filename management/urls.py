from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'management'

urlpatterns = [
    	# client urls
		url(r'^add-client/$', AddClient.as_view(), name='add_client'),
		url(r'^delete-client/(?P<pk>\d+)/$', DeleteClient.as_view(), name='delete_client'),
		url(r'^update-client/(?P<pk>\d+)/$', UpdateClient.as_view(), name='update_client'),
		url(r'^detail-client/(?P<pk>\d+)/$', DetailClient.as_view(), name='detail_client'),
		# project urls
		url(r'^add-project/(?P<pk>\d+)/$', AddProject.as_view(), name='add_project'),
		url(r'^delete-project/(?P<pk>\d+)/$', DeleteProject.as_view(), name='delete_project'),
		url(r'^update-project/(?P<pk>\d+)/$', UpdateProject.as_view(), name='update_project'),
		url(r'^detail-project/(?P<pk>\d+)/$', DetailProject.as_view(), name='detail_project'),
	]
