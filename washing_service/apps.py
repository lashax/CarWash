from django.apps import AppConfig
from django.db.utils import OperationalError


class WashingServiceConfig(AppConfig):
    name = 'washing_service'
    verbose_name = 'Washing Service'

    def ready(self):
        """
        სერვერის გაშვებისას, მარტო ერთხელ მოწმდება ScheduledOrder მოდელი.
        თუ მასში არსებული განცხადებები უკვე დასრულდა, ანუ ვისიტი იყო დაგეგმილი
        და უკვე შედგა ეს ვიზიტი, მაშინ ეს განცხადება გადადის History მოდელში.
        """

        try:
            from washing_service.models import ScheduledOrder, History
            from datetime import datetime, timezone

            schedules = ScheduledOrder.objects.all()
            dt = datetime.now()
            dt = dt.replace(tzinfo=timezone.utc)
            for schedule in schedules:
                if schedule.date < dt:
                    schedule.delete()
                    hist = History(customer=schedule.customer,
                                   location=schedule.location,
                                   car_type=schedule.car_type,
                                   car_brand=schedule.car_brand,
                                   date=schedule.date,
                                   phone=schedule.phone,
                                   washer=schedule.washer)
                    hist.save()

        except OperationalError:
            """
            ეს error ვარდება მაშინ, როცა ბაზიდან ინფორმაციას სწორად ვერ
            იღებს. ამის მიზეზი არის ScheduleOrder ან History მოდულის შეცვლა
            makemigrations/migrate კომანდის გამოყენების გარეშე.
            """
            pass
