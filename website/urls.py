from django.conf.urls import url, include

from .views import HomePageView

# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
    	# General Page Views
		url(r'^$', HomePageView.as_view(), name='homepage_view'),
]
