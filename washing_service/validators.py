from datetime import datetime, timedelta, timezone

from django.core.exceptions import ValidationError
from django.utils import timezone as djtimezone


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
