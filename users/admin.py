from django.contrib import admin

from .models import UserBase, Address

# Register your models here.

admin.site.register(UserBase)
admin.site.register(Address)