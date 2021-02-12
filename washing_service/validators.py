from datetime import datetime, timedelta, timezone

from django.core.exceptions import ValidationError
from django.utils import timezone as djtimezone

import washing_service.models


def validate_date(value: datetime) -> None:
    """
    Value should be greater than current time and less than
    a year from now.

    Otherwise, raise Validation Error.
    """
    if value < djtimezone.now():
        raise ValidationError('No time travel, sorry.', code='invalid_date')

    one_year_future = datetime.now() + timedelta(days=365)
    one_year_future = one_year_future.replace(tzinfo=timezone.utc)
    if value > one_year_future:
        raise ValidationError('We only accept orders within a year!',
                              code='invalid_date')


def validate_phone(value: str) -> None:
    """
    Phone number should be Georgian. Also, it should only contain
    digits, other than plus sign for country code (+) and
    dashes (-).
    """
    if not value.strip(' +').replace('-', '').isnumeric():
        raise ValidationError('Your phone number should only contain '
                              'digits!', code='only_digits')

    if len(value.strip(' +').replace('-', '')) not in (9, 12):
        # length of phone number is 12 if it starts with 995 and it's 9 if not
        raise ValidationError('Incorrect phone number!',
                              code='invalid_phone')


def unique_brand(value: str) -> None:
    """
    Validate that given value for car brand is not already in database.
    Model's 'unique' parameter is not used, as it checks for case sensitive
    string, which is not enough. Thus, iexact lookup has been used.
    """
    if washing_service.models.CarBrand.objects.filter(brand__iexact=value):
        raise ValidationError(f'"{value}" already exists!',
                              code='already_exists')


def validate_gender(value: str) -> None:
    """
    Validate that gender field of washing_service.models.Washer is correctly
    inputted. Only accepted values are 'M' or 'F'.
    """
    if value.upper() not in ('M', 'F'):
        raise ValidationError("Input 'M' or 'F'", code='invalid_gender')
