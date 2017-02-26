"""
Just a sample test using Client
"""
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from borrow import models


class TestPagesByClient(TestCase):
    fixtures = ['user.json']

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        super(TestPagesByClient, cls).setUpClass()

    def test_register_company(self):
        self.user = User.objects.get(username='test_user')
        self.client.login(
            username=self.user.username, password='q1')
        name = 'Test Ltd'
        address = '10 Downing Street, London'
        postcode = 'SW1A 2AA'
        sector = 'retail'
        crn = '01234567'
        self.client.post(
            reverse('company_new'),
            {
                'name': name,
                'address': address,
                'postcode': postcode,
                'registration_number': crn,
                'sector': sector,
            }
        )
        created_company = models.Company.objects.get(
            registration_number=crn)
        self.assertEqual(name, created_company.name)
        self.assertEqual(address, created_company.address)
        self.assertEqual(postcode, created_company.postcode)
        self.assertEqual(sector, created_company.sector)
