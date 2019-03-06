from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'financial'

urlpatterns = [
		# client costs
		url(r'^add-cost/(?P<pk>\d+)/$', AddClientCost.as_view(), name='add'),
		url(r'^remove-cost/(?P<pk>\d+)/$', DeleteClientCost.as_view(), name='delete'),
		url(r'^update-cost/(?P<pk>\d+)/$', UpdateClientCost.as_view(), name='update'),
		#company costs
		url(r'^add-company-cost/(?P<pk>\d+)/$', AddCompanyCost.as_view(), name='add_company_cost'),
		url(r'^remove-company-cost/(?P<pk>\d+)/$', DeleteCompanyCost.as_view(), name='delete_company_cost'),
		url(r'^update-company-cost/(?P<pk>\d+)/$', UpdateCompanyCost.as_view(), name='update_company_cost'),
		#cost details
		url(r'^cost/(?P<pk>\d+)/(?P<type>\w+)/$', CostView.as_view(), name='cost'),
		#estimted cost generator
		url(r'^estimate-cost/(?P<pk>\d+)/$', EstimatedCostGenerator.as_view(), name='estimate'),
		#CostTypes
		url(r'^add-type/(?P<pk>\d+)/$', AddCostType.as_view(), name='add_cost_type'),
		url(r'^update-type/(?P<pk>\d+)/$', UpdateCostType.as_view(), name='update_cost_type'),
		url(r'^delete-type/(?P<pk>\d+)/$', DeleteCostType.as_view(), name='delete_cost_type'),
		#services
		url(r'^add-service/(?P<pk>\d+)/$', AddService.as_view(), name='add_service'),
		url(r'^update-service/(?P<pk>\d+)/$', UpdateService.as_view(), name='update_service'),
		url(r'^delete-service/(?P<pk>\d+)/$', DeleteService.as_view(), name='delete_service'),
		#invoices
		url(r'^invoices/(?P<pk>\d+)/$', ManageInvoices.as_view(), name='invoice'),
		url(r'^invoice-items/(?P<pk>\d+)/(?P<id>\w+)/$', InvoiceDetails.as_view(), name='invoice_items'),
		url(r'^create-invoice/$', AddInvoice.as_view(), name='create_invoice'),
		url(r'^update-invoice/$', UpdateInvoice.as_view(), name='update_invoice'),
]
