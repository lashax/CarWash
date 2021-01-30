from django.contrib import admin
from .models import *

admin.site.register(WashingCenter)
admin.site.register(Manager)
admin.site.register(Washer)
admin.site.register(History)
admin.site.register(ScheduledOrder)
