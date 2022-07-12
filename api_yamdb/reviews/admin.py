from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'role',
        'bio',
        'email',
        'confirmation_code',
    )
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
