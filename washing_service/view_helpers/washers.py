from datetime import datetime

from django.db.models import Count, Q

from washing_service.models import CarType, Washer


def earning_by_time(filter_arg):
    """
    Given 'filter_arg' variable, which is either
    year, month, week or overall, calculate each washers' earning by
    its' corresponding interval.

    Return QuerySet object of Washer, where each data has added
    attribute named corresponding to filter_arg (so if we are filtering
    with month, attribute name will be month). This data stores value in integer
    as to how much has the washer earned in the given interval.
    """

    if filter_arg == 'year':
        current = datetime.now().year
    elif filter_arg == 'month':
        current = datetime.now().month
    elif filter_arg == 'week':
        current = datetime.now().isocalendar()[1]
    elif filter_arg == 'overall':
        earning = Washer.objects.annotate(
            overall=10 * Count('history', filter=
            Q(history__car_type=CarType.objects.get(type='Sedan')))
                    + 15 * Count('history', filter=Q(
                history__car_type=CarType.objects.get(type='Minivan')))
                    + 20 * Count('history', filter=Q(
                history__car_type=CarType.objects.get(type='Truck')))
        )
        return earning

    history_date = f"history__date__{filter_arg}"

    earning = Washer.objects.annotate(
        **{filter_arg: 10 * Count('history', filter=
        Q(**{'history__car_type': CarType.objects.get(type='Sedan'),
             history_date: current}))
                       + 15 * Count('history', filter=Q(
            **{'history__car_type': CarType.objects.get(type='Minivan'),
               history_date: current}))
                       + 20 * Count('history', filter=Q(
            **{'history__car_type': CarType.objects.get(type='Truck'),
               history_date: current}))}
    )

    return earning
