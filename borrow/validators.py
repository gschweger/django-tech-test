"""
Validator functions for models inputs
"""
import re
from django.core.exceptions import ValidationError
from ukpostcodeutils import validation


def validate_crn(crn: str):
    """
    Validate CRN (Company Registration Number)

    Companies formed in England and Wales have CRNs
    beginning with 0 (zero).
    Scottish companies are given CRNs with the prefix ‘SC’.
    Limited Liability Partnerships (LLPs) are issued with
    CRNs beginning with ‘OC’.
    Scottish LLPs have CRNs beginning with ‘SO’.

    Args:
        crn: string Company Registration number

    Raises:
        Validation Error:

    Returns:
        None:
    """
    patterns = {
        r'^0\d{7}$',  # English CRN
        r'^SC\d{6}',  # Scottish CRN
        r'^OC\d{6}',  # LLP CRN
        r'^SO\d{6}'  # Scottish LLP CRN
    }

    match = False

    for pattern in patterns:
        if re.match(pattern, crn):
            match = True
            break
    if not match:
        raise ValidationError(
            'This cannot be a valid Company Registration Number: '
            '%s' % crn)


def validate_postcode(postcode: str):
    """
    Validate UK postcode format

    Args:
        postcode: string
    Raises:

        Validation Error:

    Returns:
        None:
    """
    postcode_no_spaces = postcode.replace(' ', '')
    if not validation.is_valid_postcode(postcode_no_spaces):
        raise ValidationError(
            'This cannot be a valid postcode: %s' % postcode)
