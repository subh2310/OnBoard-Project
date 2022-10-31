from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.validators import (validate_store_merchant,
                                 validate_items_merchant, validate_total_cost)
from accounts.models import (Merchant, Item, Store, Order)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all(), message='User with this email already exists.')])

    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password1', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password1'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('pk', 'name', 'email', 'phone', 'created_at')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('pk', 'name', 'merchant', 'cost',
                  'description', 'created_at')


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('pk', 'name', 'merchant', 'address', 'lon',
                  'lat', 'active', 'items', 'created_at')

    def validate(self, data):
        """
        Perform object level validation for Merchant Integrity during Store
        Creation.

        validate_items_merchant : Checks if the Items' Merchant is same as
        Order's Merchant.
        """

        validate_items_merchant(data)

        return data


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('pk', 'merchant', 'store', 'total_cost',
                  'status', 'items', 'created_at')

    def validate(self, data):
        """
        Perform object level validation for Merchant Integrity during Order
        Creation.

        Contains below functions :-
        1. validate_store_merchant : Checks if the Store's Merchant is same as
        Order's Merchant.
        2. validate_items_merchant : Checks if the Items' Merchant is same as
        Order's Merchant.
        3. validate_total_cost : Checks if the Sum of Item Costs is equal to
        Total Cost
        """

        validate_store_merchant(data)
        validate_items_merchant(data)
        validate_total_cost(data)

        return data

