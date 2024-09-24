from django.contrib import admin

from django.contrib import admin
from .models import User, Reporte, Actividad

admin.site.register(User)
admin.site.register(Reporte)
admin.site.register(Actividad)
