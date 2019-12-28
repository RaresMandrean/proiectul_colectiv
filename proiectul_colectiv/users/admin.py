from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Profile
from users.forms import UserRegisterForm, UserUpdateForm


class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    form = UserUpdateForm
    model = CustomUser
    list_display = ['email', 'username']


admin.site.register(Profile)
admin.site.register(CustomUser, CustomUserAdmin)
