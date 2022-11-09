import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from api.models import Items, Profile, Stores

client = APIClient()
User = get_user_model()

# Merchant Login & Registration Test Case
@pytest.mark.django_db
def test_merchant_registration():
    payload = {"username" : "merchant", "email" : "merchant@gmail.com", "password" : "password@123", "profile.name" : "Merchant_User", "profile.role" : 1}
    response = client.post("/register/", payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_merchant_login(merchant_data):
    response = client.post("/login/", dict(username = "merchant", password = "password@123"))
    assert response.status_code == 200

# Stores Creation EndPoint Test Case
@pytest.mark.django_db
def test_store_creation_api_endpoint(merchant_data):
    # import pdb; pdb.set_trace()
    response = client.post("/login/", dict(username = "merchant", password = "password@123"))
    token = response.data['access']
    req_send = client.post("/stores/", dict(name = "WhiteField Outlet", address = "WhiteField", lat = 13, lng = 13, merchant = merchant_data), **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201

# Items Creation Endpoint Test Case
@pytest.mark.django_db
def test_item_creation_api_endpoint(merchant_data):
    # import pdb; pdb.set_trace()
    response = client.post("/login/", dict(username = "merchant", password = "password@123"))
    token = response.data['access']
    store = Stores.objects.create(name = "WhiteField Outlet", address = "WhiteField", lat = 13, lng = 13, merchant = merchant_data)
    req_send = client.post("/items/", dict(name = "Dosa", price = 120, description = "Sambhar Dosa", stores = store), **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201


# consumer Login & Registration Test Case
@pytest.mark.django_db
def test_consumer_registration():
    payload = {"username" : "consumer", "email" : "consumer@gmail.com", "password" : "password@123", "profile.name" : "consumer_User", "profile.role" : 2}
    response = client.post("/register/", payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_consumer_login(consumer_data):
    response = client.post("/login/", dict(username = "consumer", password = "password@123"))
    assert response.status_code == 200

# Test Place Order Endpoints
@pytest.mark.django_db
def test_place_order_api_endpoints(merchant_data, consumer_data):
    # import pdb; pdb.set_trace()
    response = client.post("/login/", dict(username = "consumer", password = "password@123"))
    token = response.data["access"]
    store = Stores.objects.create(name = "WhiteField Outlet", address = "WhiteField", lat = 13, lng = 13, merchant = merchant_data)
    item = Items.objects.create(name = "Dosa", price = 120, description = "Sambhar Dosa", stores = store)
    req_send = client.post("/place_orders/", dict(user = consumer_data, merchant = merchant_data.pk, store = store.pk, items = item.pk), **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201
    items_present = set(Items.objects.all().values_list('name', flat=True))
    assert "Dosa" in items_present
