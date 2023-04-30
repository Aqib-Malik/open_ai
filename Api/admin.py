from django.contrib import admin
from Api.models import *

# Register your models here.
admin.site.register([Appointment,Role,Hospital,Permission,Patient])
