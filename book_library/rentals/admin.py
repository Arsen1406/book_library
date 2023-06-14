from django.contrib import admin
from rentals.models import Rentals


class RentalsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'reader', 'create_date', 'return_date',)
    search_fields = ('reader',)
    filter_horizontal = ('books',)
    empty_value_display = '-пусто-'


admin.site.register(Rentals, RentalsAdmin)
