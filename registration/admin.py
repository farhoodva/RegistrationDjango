from django.contrib import admin
from.forms import DriverInfoForm
from .models import (
    DriverInfo,
    City,
    State,
)


class DriverInfoAdmin(admin.ModelAdmin):
    form = DriverInfoForm
    list_display = ['national_id', 'smart_card_number', 'name', 'family', 'cellnumber', 'email', 'state', 'city',
                    'date_added']
    search_fields = ['national_id']
    empty_value_display = 'Not available'


class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    sortable_by = 'name'


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']
    sortable_by = 'name'


admin.site.register(City, CityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(DriverInfo, DriverInfoAdmin)






