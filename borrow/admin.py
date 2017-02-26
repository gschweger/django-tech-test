from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from borrow.models import (
    Borrower, Company, MapUserToCompany, LoanRequest)


class BorrowerInline(admin.StackedInline):
    model = Borrower
    can_delete = False
    verbose_name_plural = 'Borrowers'


class UserAdmin(BaseUserAdmin):
    inlines = (BorrowerInline, )


class MapUserToCompanyInline(admin.TabularInline):
    model = MapUserToCompany
    readonly_fields = ('created_at',)
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    model = Company
    inlines = (MapUserToCompanyInline,)

    list_display = ('name', 'registration_number',
                    'address', 'postcode', 'sector',)
    list_filter = ['sector']
    search_fields = [
        'name', 'registration_number',
        'address', 'postcode'
    ]


class LoanRequestAdmin(admin.ModelAdmin):
    model = LoanRequest

    list_display = (
        'amount', 'days',
        'borrower', 'created_at', 'status',)
    list_filter = ['status', 'days']
    search_fields = [
        'amount', 'days', 'created_at', 'status']
    readonly_fields = ('created_at',)


class MapUserToCompanyAdmin(admin.ModelAdmin):
    model = MapUserToCompany
    list_display = ('user', 'company', 'created_at',
                    'confirmed_by_admin')
    list_filter = ('user', 'company', 'created_at',
                   'confirmed_by_admin')
    search_fields = ['user', 'company']

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(MapUserToCompany, MapUserToCompanyAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)
