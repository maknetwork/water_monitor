from django.contrib import admin
from .models import Device, Setup, Zone, Value
# Register your models here.
admin.site.register(Device)
admin.site.register(Setup)
admin.site.register(Zone)
admin.site.register(Value)
