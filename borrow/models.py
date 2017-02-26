from django.contrib.auth.models import User
from django.db import models

from borrow import validators


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=24, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Company(models.Model):
    _sector_choices = (
        ('retail', 'Retail'),
        ('professional_services', 'Professional Services'),
        ('food_and_drink', 'Food & Drink'),
        ('entertainment', 'Entertainment'),
    )
    name = models.CharField(
        max_length=64, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    postcode = models.CharField(
        max_length=8, null=False, blank=False,
        validators=[validators.validate_postcode])
    registration_number = models.CharField(
        max_length=8, null=False, blank=False, unique=True,
        validators=[validators.validate_crn])
    sector = models.CharField(
        max_length=24, null=False, blank=False,
        choices=_sector_choices)
    users = models.ManyToManyField(
        User, blank=True,
        through='borrow.MapUserToCompany')

    class Meta:
        ordering = ['name']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class MapUserToCompany(models.Model):
    """
    This model is used for ManyToMany relation between
    Borrower and Company.
    """
    user = models.ForeignKey(
        User, null=False, blank=False, db_index=True)
    company = models.ForeignKey(
        Company, null=False, blank=False, db_index=True)
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True)
    confirmed_by_admin = models.BooleanField(
        default=True, db_index=True)

    class Meta:
        unique_together = ['user', 'company']
        ordering = ['user', 'created_at', 'company']
        verbose_name = 'Map User to Company'
        verbose_name_plural = 'Map Users to Companies'

    def __str__(self):
        return "%s %s" % (self.user, self.company)


class LoanRequest(models.Model):
    _status_choices = (
        ('received', 'Received'),
        ('processing', 'Processing'),
        ('declined', 'Declined'),
        ('approved', 'Approved')
    )
    amount = models.DecimalField(
        null=False, blank=False, max_digits=10, decimal_places=2,
        help_text='Amount of the loan')
    days = models.PositiveSmallIntegerField(
        null=False, blank=False,
        help_text='How many days?')
    reason = models.TextField(
        null=False, blank=False,
        help_text='Reason for the loan')
    borrower = models.ForeignKey(
        MapUserToCompany, null=False, blank=False)
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=False,
        db_index=True)
    status = models.CharField(
        max_length=16, null=False, blank=False,
        choices=_status_choices, default='received')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '%s: %s (%s days)' % (
            self.borrower.user.get_full_name(), self.amount, self.days)
