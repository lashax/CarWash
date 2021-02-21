from datetime import datetime
from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Page
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


def create_query_set(objects_page: Page) -> QuerySet:
    """
    Given Page object, firstly create list of ids for each object on that page,
    then generate QuerySet for that objects.
    """
    objects_ids = [obj.id for obj in objects_page]
    query_set = Washer.objects.filter(id__in=objects_ids)

    return query_set


def earning_by_time(filter_arg: str, objects_page: Page) -> QuerySet:
    """
    'filter_arg': either year, month, week or overall
    'objects_page': page, where current page's washers are stored
                    when iterated over

    Return QuerySet object of washers of the current page,
    where each data has added attribute named corresponding to
    filter_arg (so if we are filtering with month, attribute name
    will be month). This data stores value in decimal as to how much has
    the washer earned in the given interval, also considering salary %.

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

    # QuerySet of current page's washers
    current_washers = create_query_set(objects_page)

    earning = current_washers.annotate(
        **{filter_arg: (earning_by_sedan + earning_by_minivan +
                        earning_by_truck) * F('salary') / 100})

    return earning


def get_washer_query(request: WSGIRequest) -> Union[list, QuerySet]:
    """
    Given request, generate QuerySet or list of Washer objects which will then
    be displayed on the page.

    This function is used to filter results by washer name if user uses search
    box.
    """
    query = request.GET.get('q')

    # if in the current request user did not search for anything
    if not query:
        return Washer.objects.all()

    queryset = []
    queries = query.split()
    for q in queries:
        washers = Washer.objects.filter(full_name__icontains=q)

        for washer in washers:
            queryset.append(washer)

    return list(set(queryset))
