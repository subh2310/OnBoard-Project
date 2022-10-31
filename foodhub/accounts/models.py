from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=150, blank=True, null=True, unique=True)
    USERNAME_FIELD = 'email'
    is_active = models.BooleanField(default=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users'

# Field Choices

class OrderStatus(models.TextChoices):
    ACTIVE = 'ACT', 'Active'
    CANCELLED = 'CAN', 'Cancelled'
    FINISHED = 'FIN', 'Finished'


# Table Models

class Merchant(models.Model):
    """
    Merchants like KFC etc are represented by this model.

    Optional Fields : Email
    """
    name = models.CharField("Name", max_length=150)
    email = models.EmailField("Email", max_length=254, blank=False)
    phone = models.CharField("Phone", max_length=20)
    created_at = models.DateTimeField(
        "Created At", auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='merchant_created_by', null=True)
    updated_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='merchant_updated_by', null=True)


    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Food Items are represented by this model.

    Optional Fields : Description
    """
    name = models.CharField("Name", max_length=200)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    cost = models.DecimalField("Cost", max_digits=10, decimal_places=2)
    description = models.TextField("Description", blank=True)
    created_at = models.DateTimeField(
        "Created At", auto_now_add=True, null=True)
    active = models.BooleanField("Active", default=False)
    created_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='item_created_by', null=True)
    updated_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='item_updated_by', null=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    """
    Merchant's stores are represented by this model.

    Optional Fields : address, lon(longitude), lat(latitude)
    """
    name = models.CharField("Name", max_length=150)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    address = models.TextField("Address", blank=True)
    lon = models.FloatField("Longitude", blank=True, null=True)
    lat = models.FloatField("Latitude", blank=True, null=True)
    active = models.BooleanField("Active", default=False)
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(
        "Created At", auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='store_created_by', null=True)
    updated_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='store_updated_by', null=True)

    def __str__(self):
        return f'{self.merchant} : {self.name}'


class Order(models.Model):
    """
    Orders are represented by this model.
    """
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_cost = models.DecimalField(
        "Total Cost", max_digits=10, decimal_places=2)
    status = models.CharField("Order Status",
                              max_length=100,
                              choices=OrderStatus.choices,
                              default=OrderStatus.ACTIVE)
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(
        "Created At", auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='order_created_by', null=True)
    updated_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='order_updated_by', null=True)
