from django.core.exceptions import ValidationError
from django.test import TestCase

from borrow import validators


class TestValidateCRN(TestCase):

    def test_valid_crn(self):
        """ Test valid CRNs """
        crns = {
            '01234567',
            'SC123456',
            'OC654321',
            'SO987654'
        }
        for crn in crns:
            self.assertIsNone(
                validators.validate_crn(crn))

    def test_not_valid_crn(self):
        """ Test not valid CRNs """
        crns = {
            'AAAAAAAA',
            '12345678',
            '012345678',
            '0S123456',
            '1',

        }
        for crn in crns:
            error_message = 'This cannot be a valid ' \
                            'Company Registration Number: ' \
                            '%s' % crn
            with self.assertRaisesMessage(ValidationError, error_message):
                validators.validate_crn(crn)


class TestValidatePostcode(TestCase):

    def test_valid_postcode(self):
        """ Test valid postcodes """
        postcodes = {
            'SE26 4QT',
            'SE264QT',
            'SE17NX',
            'WC2H 9QL',
            'WC2H9QL'
        }
        for postcode in postcodes:
            self.assertIsNone(
                validators.validate_postcode(postcode))

    def test_invalid_postcode(self):
        """ Test invalid postcode """
        postcodes = {
            'AAAAAAAA',
            '12345678',

        }
        for postcode in postcodes:
            error_message = 'This cannot be a valid ' \
                            'postcode: %s' % postcode
            with self.assertRaisesMessage(ValidationError, error_message):
                validators.validate_postcode(postcode)
