from django import forms
from borrow import models


class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = models.LoanRequest
        fields = ['amount', 'days', 'reason', 'borrower']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LoanRequestForm, self).__init__(*args, **kwargs)
        self.fields["borrower"].queryset = \
            models.MapUserToCompany.objects.filter(user=self.request.user)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ['name', 'address', 'postcode', 'registration_number',
                  'sector']


class PhoneForm(forms.ModelForm):
    class Meta:
        model = models.Borrower
        fields = ['phone_number']
