from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'financial'

urlpatterns = [
		# costs views
		url(r'^add-cost/(?P<pk>\d+)/$', AddCost.as_view(), name='add'),
		url(r'^add-company-cost/(?P<pk>\d+)/$', AddCompanycost.as_view(), name='add_company_cost'),
		url(r'^remove-cost/(?P<pk>\d+)/$', DeleteCost.as_view(), name='delete'),
		url(r'^update-cost/(?P<pk>\d+)/$', UpdateCost.as_view(), name='update'),
		url(r'^cost/(?P<pk>\d+)/(?P<type>\w+)/$', CostView.as_view(), name='cost'),
		url(r'^estimate-cost/$', EstimatedCostGenerator.as_view(), name='estimate'),
		#services
		url(r'^add-service/(?P<pk>\d+)/$', AddService.as_view(), name='add_service'),
		url(r'^update-service/(?P<pk>\d+)/$', UpdateService.as_view(), name='update_service'),
		url(r'^delete-service/(?P<pk>\d+)/$', DeleteService.as_view(), name='delete_service'),
		#invoices
		url(r'^invoices/$', ManageInvoices.as_view(), name='invoice'),
		url(r'^invoice-items/(?P<id>\w+)/$', InvoiceDetails.as_view(), name='invoice_items'),
		url(r'^create-invoice/$', AddInvoice.as_view(), name='create_invoice'),
		url(r'^update-invoice/$', UpdateInvoice.as_view(), name='update_invoice'),
]
