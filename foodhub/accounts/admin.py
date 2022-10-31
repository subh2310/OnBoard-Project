from django.contrib import admin
from accounts.models import Merchant, Item, Store, Order, User
# Register your models here.

models_iterable = [Merchant, Item, Store, Order, User]

admin.site.register(models_iterable)
