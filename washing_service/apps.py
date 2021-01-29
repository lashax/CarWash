from django.apps import AppConfig


class WashingServiceConfig(AppConfig):
    name = 'washing_service'
    verbose_name = 'Washing Service'

    def ready(self):
        """
        სერვერის გაშვებისას, მარტო ერთხელ მოწმდება ScheduledOrders მოდელი.
        თუ მასში არსებული განცხადებები უკვე დასრულდა, ანუ ვისიტი იყო დაგეგმილი
        და უკვე შედგა ეს ვიზიტი, მაშინ ეს განცხადება გადადის History მოდელში.
        """

        from washing_service.models import ScheduledOrders, History
        from datetime import datetime
        from datetime import timezone

        schedules = ScheduledOrders.objects.all()
        dt = datetime.now()
        dt = dt.replace(tzinfo=timezone.utc)
        for schedule in schedules:
            if schedule.date < dt:
                schedule.delete()
                hist = History(customer=schedule.customer,
                               location=schedule.location,
                               car=schedule.car, date=schedule.date,
                               phone=schedule.phone)
                hist.save()
