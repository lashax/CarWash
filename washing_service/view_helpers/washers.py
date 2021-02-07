from datetime import datetime
from typing import Union

from django.db.models import Count, Q, F, DecimalField, QuerySet

from washing_service.models import Washer

SEDAN_EARNING = 10
MINIVAN_EARNING = 15
TRUCK_EARNING = 20


def gen_query(car_type: str, history_date: str,
              time_interval: Union[int, None]) -> Q:
    """
    Generate query, Q object which will be passed to Count class as
    filter argument.

    car_type is type of a car with which to filter history. This should be
    one of: 'Sedan', 'Minivan, 'Truck'.

    If time_interval parameter is None, that means query is used
    to find out overall salary of an user, in which case history is not
    filtered with date.

    return Q object.
    """
    if time_interval:
        return Q(**{
            'history__car_type__type': car_type,
            history_date: time_interval
        })
    else:
        return Q(**{'history__car_type__type': car_type})


def earning_by_car(car_type: str, history_date: str,
                   time_interval: Union[int, None]) -> Count:
    """
    Calculate money earned for given car type.

    car_type is type of a car with which to filter history. This should be
    one of: 'Sedan', 'Minivan, 'Truck'.

    For sedan, per wash costs 10₾, for minivan 15₾ and for truck 20₾.

    Return CombinedExpression, which is Count object multiplied
    by value (10, 15 or 20).
    """
    car_earning = Count('history', filter=
                        gen_query(car_type, history_date, time_interval),
                        output_field=DecimalField())
    price_per_wash = {
        'Sedan': SEDAN_EARNING,
        'Minivan': MINIVAN_EARNING,
        'Truck': TRUCK_EARNING
    }
    car_earning *= price_per_wash.get(car_type)

    return car_earning


def earning_by_time(filter_arg: str) -> QuerySet:
    """
    Given 'filter_arg' variable, which is either
    year, month, week or overall, calculate each washers' earning by
    its' corresponding interval.

    Return QuerySet object of Washer, where each data has added
    attribute named corresponding to filter_arg (so if we are filtering
    with month, attribute name will be month). This data stores value in decimal
    as to how much has the washer earned in the given interval, also considering
    salary %.

    Note, that even though type of new attribute is decimal, it will never
    have fractional part because we are diving the last result by 100,
    which is an integer.
    """
    time_dict = {
        'overall': None,
        'year': datetime.now().year,
        'month': datetime.now().month,
        'week': datetime.now().isocalendar()[1]
    }

    time_interval = time_dict.get(filter_arg)
    history_date = f"history__date__{filter_arg}"

    earning_by_sedan = earning_by_car('Sedan', history_date, time_interval)
    earning_by_minivan = earning_by_car('Minivan', history_date, time_interval)
    earning_by_truck = earning_by_car('Truck', history_date, time_interval)

    earning = Washer.objects.annotate(
        **{filter_arg: (earning_by_sedan + earning_by_minivan +
                        earning_by_truck) * F('salary') / 100})

    return earning
