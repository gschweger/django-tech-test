from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from django.utils.decorators import method_decorator

from borrow.forms import LoanRequestForm, CompanyForm, PhoneForm
from borrow.models import (
    LoanRequest, MapUserToCompany, Company, Borrower)


@login_required()
def home_page(request):
    context = {}
    context['page_title'] = 'Home'
    return render(request, 'home.html', context=context)


class LoanRequestListPage(ListView):
    template_name = 'loan_requests.html'
    model = LoanRequest

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoanRequestListPage, self).dispatch(*args, **kwargs)

    def get_list(self):
        list_data = self.model.objects.filter(
            borrower__user=self.request.user,
        ).order_by('-created_at')
        return list_data

    def get_context_data(self, **kwargs):
        context = super(LoanRequestListPage, self).get_context_data(**kwargs)
        context["items"] = self.get_list()
        context["page_title"] = "Loan requests"
        return context

    def get_template_names(self):
        return ['loan_requests.html']


@login_required()
def loan_request_new(request):
    context = {}
    context['page_title'] = 'New Loan Request'
    if request.method == 'POST':
        context['form'] = LoanRequestForm(request.POST, request=request)
        if context['form'].is_valid():
            map_obj = MapUserToCompany.objects.get(
                id=request.POST['borrower'])
            LoanRequest.objects.create(
                amount=request.POST['amount'],
                days=request.POST['days'],
                reason=request.POST['reason'],
                borrower=map_obj
            )
            return HttpResponseRedirect(reverse('loan_request_list'))
    else:
        context['form'] = LoanRequestForm(request=request)

    return render(request, 'loan_request_new.html', context=context)


class CompanyListPage(ListView):
    template_name = 'companies.html'
    model = Company

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CompanyListPage, self).dispatch(*args, **kwargs)

    def get_list(self):
        map_objects = MapUserToCompany.objects.filter(
            user=self.request.user
        ).values('company__registration_number')
        list_data = self.model.objects.filter(
            registration_number__in=map_objects,
        ).order_by('name')
        return list_data

    def get_context_data(self, **kwargs):
        context = super(CompanyListPage, self).get_context_data(**kwargs)
        context["items"] = self.get_list()
        context["page_title"] = "Companies"
        return context


@login_required()
def company_new(request):
    context = {}
    context['page_title'] = 'New Company'
    if request.method == 'POST':
        context['form'] = CompanyForm(request.POST)
        if context['form'].is_valid():
            Company.objects.create(
                name=request.POST['name'],
                address=request.POST['address'],
                postcode=request.POST['postcode'],
                registration_number=request.POST['registration_number'],
                sector=request.POST['sector']
            )
            return HttpResponseRedirect(reverse('company_list'))
    else:
        context['form'] = CompanyForm()

    return render(request, 'company_new.html', context=context)


@login_required()
def phone(request):
    context = {}
    context['page_title'] = 'Your phone number'
    if request.method == 'POST':
        context['form'] = PhoneForm(request.POST)
        if context['form'].is_valid():
            borrower = Borrower.objects.get_or_create(
                user=request.user)[0]
            borrower.phone_number = request.POST['phone_number']
            borrower.save()
            return HttpResponseRedirect(reverse('company_list'))
    else:
        borrower = Borrower.objects.get_or_create(
            user=request.user)[0]

        context['form'] = PhoneForm(
            {"phone_number": borrower.phone_number})

    return render(request, 'phone.html', context=context)
