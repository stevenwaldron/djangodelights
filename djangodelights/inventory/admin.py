from django.contrib import admin
from .models import Ingredient, MenuItem, Purchase
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(Purchase)
