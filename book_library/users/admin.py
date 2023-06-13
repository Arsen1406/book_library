from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',)
    empty_value_display = '-пусто-'


admin.site.register(User, UsersAdmin)
