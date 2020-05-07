from django.contrib import admin
from .models import Amplifier, Modelo, State

# Register your models here.
admin.site.register(Amplifier)
admin.site.register(Modelo)
admin.site.register(State)