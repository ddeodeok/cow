from django.contrib import admin
from .models import Cow, Pre_childbirth, Estrus, Event, Sensor, SensorID



class CowAdmin(admin.ModelAdmin):
    search_fields=['cow_num']
admin.site.register(Cow,CowAdmin)


# Register your models here.
admin.site.register(Sensor)
admin.site.register(Pre_childbirth)
admin.site.register(Estrus)
# admin.site.register(Cow)
admin.site.register(Event)
admin.site.register(SensorID)