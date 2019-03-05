from django.conf.urls import url, include

from .views import HomePageView, NewUser

# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
    	# General Page Views
		url(r'^$', HomePageView.as_view(), name='homepage_view'),
		url(r'^register/$', NewUser.as_view(), name='register'),
]
