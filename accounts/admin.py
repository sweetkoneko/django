from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import UserAccount, Profile

# Register your models here.
admin.site.register(UserAccount, UserAdmin)
admin.site.register(Profile)