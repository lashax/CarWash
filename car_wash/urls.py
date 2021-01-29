"""car_wash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('washing_service.urls'))
]

# from washing_service.models import ScheduledOrders, History
# from datetime import datetime
# from datetime import timezone
#
#
# schedules = ScheduledOrders.objects.all()
# dt = datetime.now()
# dt = dt.replace(tzinfo=timezone.utc)
# for schedule in schedules:
#     if schedule.date < dt:
#         schedule.delete()
#         hist = History(customer=schedule.customer, location=schedule.location,
#                        car=schedule.car, date=schedule.date, phone=schedule.phone)
#         hist.save()
