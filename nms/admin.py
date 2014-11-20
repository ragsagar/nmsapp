from django.contrib import admin

from .models import (Station, Meter, MeterInfo, Log, MeterLocation,
        StationLocation, Mode, MeterConfig, StationStatus)

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    pass


@admin.register(MeterInfo)
class MeterInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(MeterLocation)
class MeterLocationAdmin(admin.ModelAdmin):
    pass

@admin.register(StationLocation)
class StationLocationAdmin(admin.ModelAdmin):
    pass

@admin.register(MeterConfig)
class MeterConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(Mode)
class ModeAdmin(admin.ModelAdmin):
    pass

@admin.register(StationStatus)
class StationStatusAdmin(admin.ModelAdmin):
    pass
