from datetime import datetime

from django.db.models import Count, Q, F, DecimalField

from washing_service.models import CarType, Washer


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

    if filter_arg == 'year':
        current = datetime.now().year
    elif filter_arg == 'month':
        current = datetime.now().month
    elif filter_arg == 'week':
        current = datetime.now().isocalendar()[1]
    elif filter_arg == 'overall':
        earning = Washer.objects.annotate(
            overall=(10 * Count('history', filter=
            Q(history__car_type=CarType.objects.get(type='Sedan')),
                                output_field=DecimalField())
                     + 15 * Count('history', filter=Q(
                        history__car_type=CarType.objects.get(type='Minivan')),
                                  output_field=DecimalField())
                     + 20 * Count('history', filter=Q(
                        history__car_type=CarType.objects.get(type='Truck')),
                                  output_field=DecimalField())) * F(
                'salary') / 100
        )
        return earning

    history_date = f"history__date__{filter_arg}"

    earning = Washer.objects.annotate(
        **{filter_arg: (10 * Count('history', filter=
        Q(**{'history__car_type': CarType.objects.get(type='Sedan'),
             history_date: current}), output_field=DecimalField())
                        + 15 * Count('history', filter=Q(
                    **{'history__car_type': CarType.objects.get(type='Minivan'),
                       history_date: current}), output_field=DecimalField())
                        + 20 * Count('history', filter=Q(
                    **{'history__car_type': CarType.objects.get(type='Truck'),
                       history_date: current}),
                                     output_field=DecimalField())) * F(
            'salary') / 100}
    )

    return earning
