from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'role', 'country', 'city', 'is_staff')
    list_filter = ('email', 'role', 'country', 'city', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
         'fields': ('role', 'phone', 'country', 'city', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'phone', 'country', 'city', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'role', 'country', 'city')
    ordering = ('email', 'role', 'country', 'city')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Client)
admin.site.register(Company)