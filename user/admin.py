from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as SuperUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(SuperUserAdmin):
    list_display = ('username', 'email', 'name',)
    readonly_fields = ('uuid', 'last_login', 'date_joined', 'change_password_link')

    @mark_safe
    def change_password_link(self, obj):
        return f"<a target='_blank' href='/admin/user/user/{obj.id}/password/'>Trocar Senha</a>"
    
    change_password_link.short_description = 'Trocar Senha'
    change_password_link.allow_tags = True