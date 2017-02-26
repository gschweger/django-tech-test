from django.conf.urls import url
from borrow import views

urlpatterns = [
    url(r'^loan_requests/$',
        views.LoanRequestListPage.as_view(),
        name='loan_request_list'),
    url(r'^loan_requests/new/$',
        views.loan_request_new,
        name='loan_request_new'),
    url(r'^companies/$',
        views.CompanyListPage.as_view(),
        name='company_list'),
    url(r'^company/new/$',
        views.company_new,
        name='company_new'),
    url(r'^phone/$',
        views.phone,
        name='phone'),
]
