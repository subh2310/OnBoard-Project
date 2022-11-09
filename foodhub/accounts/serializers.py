from cgitb import lookup
from dataclasses import field
from enum import unique
from tkinter.tix import Tree
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("name", "role",)


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "profile",
        )

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact = lower_email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return lower_email

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User.objects.create(
            username = validated_data["username"],
            email = validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        Profile.objects.create(user = user, **profile_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 128)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.pop('username')
        password = data.pop('password')
        user = authenticate(username = username, password = password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username
            }
            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class UserChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)            

class ItemSerializers(serializers.ModelSerializer):
    stores = serializers.SlugRelatedField(slug_field = 'name', queryset = Stores.objects.all())
    class Meta:
        model = Items
        fields = ['id', 'name', 'price', 'description', 'stores']

class StoresSerializer(serializers.ModelSerializer):
    merchant = serializers.StringRelatedField(read_only = True)
    items = ItemSerializers(many = True, read_only = True)
    class Meta:
        model = Stores
        fields = ["merchant", "name", "address", "lat", "lng", "items"]
        extra_kwargs = {"merchant": {"read_only": True}}

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    # items = serializers.SlugRelatedField(slug_field = "name", many = True, queryset = Items.objects.all())

    def get_fields(self, *args, **kwargs):
        fields = super(OrderSerializer, self).get_fields(*args, **kwargs)
        fields['merchant'].queryset = fields['merchant'].queryset.filter(role = 1)
        return fields

    def to_representation(self, instance):
        response = super().to_representation(instance)
        print("-----------------------------------------")
        print(response)
        print("-----------------------------------------")
        # response['store'] = StoresSerializer(instance.store).data['name']
        # response['merchant'] = ProfileSerializer(instance.merchant).data['name']
        return response

    class Meta:
        model = Orders
        fields = ['id', 'user', 'merchant', 'store', 'items']

class ViewConsumerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('username', 'email', 'profile')
