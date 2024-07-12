from django.contrib import admin
from .models import Appointment, Response, Doctor, Bill

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Response)
admin.site.register(Doctor)
admin.site.register(Bill)
