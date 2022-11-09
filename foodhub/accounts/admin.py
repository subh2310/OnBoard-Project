from django.contrib import admin
from api.models import Items, Orders, Profile, Stores
admin.site.register([Profile, Stores, Items, Orders])
