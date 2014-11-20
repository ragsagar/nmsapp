from django.contrib import admin

from .models import Station, Meter, MeterInfo

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    pass


@admin.register(MeterInfo)
class MeterInfoAdmin(admin.ModelAdmin):
    pass
