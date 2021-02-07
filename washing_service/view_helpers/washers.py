from datetime import datetime

from django.db.models import Count, Q, F, DecimalField

from washing_service.models import CarType, Washer


def gen_query(car_type, history_date, time_interval):
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
            'history__car_type': CarType.objects.get(type=car_type),
            history_date: time_interval
        })
    else:
        return Q(**{'history__car_type': CarType.objects.get(type=car_type)})


def earning_by_time(filter_arg):
    """
    Given 'filter_arg' variable, which is either
    year, month, week or overall, calculate each washers' earning by
    its' corresponding interval.

    Return QuerySet object of Washer, where each data has added
    attribute named corresponding to filter_arg (so if we are filtering
    with month, attribute name will be month). This data stores value in decimal
    as to how much has the washer earned in the given interval, also considering
    salary %.
    """
    time_dict = {
        'overall': None,
        'year': datetime.now().year,
        'month': datetime.now().month,
        'week': datetime.now().isocalendar()[1]
    }

    time_interval = time_dict.get(filter_arg)
    history_date = f"history__date__{filter_arg}"

    earning_by_sedan = 10 * Count('history', filter=gen_query(
                                  'Sedan', history_date, time_interval),
                                  output_field=DecimalField())

    earning_by_minivan = 15 * Count('history', filter=gen_query(
                                    'Minivan', history_date, time_interval),
                                    output_field=DecimalField())

    earning_by_truck = 20 * Count('history', filter=gen_query(
                                  'Truck', history_date, time_interval),
                                  output_field=DecimalField())

    earning = Washer.objects.annotate(
        **{filter_arg: (earning_by_sedan + earning_by_minivan +
                        earning_by_truck) * F('salary') / 100})

    return earning
