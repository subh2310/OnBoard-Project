from urllib import response
import pytest
from rest_framework.test import APIClient

from accounts.models import Merchant, Item, Store, Order

client=APIClient()

@pytest.mark.django_db
def test_register_user(client):
    payload= dict(
        password1="subh@2310",
        password2="subh@2310",
        email="subhnesh0@gmail.com",
        first_name="Subhnesh",
        last_name="Kumar"
    )
    response = client.post('/account/register/', payload)
    data=response.data

    assert data['first_name'] == payload['first_name']
    assert response.status_code == 201

@pytest.mark.django_db
def test_login_user(user, client):
    response = client.post('/account/login/', dict(email="subhnesh0@gmail.com", password="subh@2310"))
    assert response.status_code == 200



@pytest.mark.django_db
def test_merchant_creation_api_endpoint(user):
    # import pdb; pdb.set_trace()
    response = client.post("/account/login/", dict(email = "subhnesh0@gmail.com", password = "subh@2310"))
    token = response.data['access']
    payload= dict(
        name = "Kfc", email ="kfc1@gmail.com", phone='789678987'
    ) 
    response=client.post("/account/merchants/", payload, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert response.status_code == 201

@pytest.mark.django_db
def test_item_creation_api_endpoint(user,add_merchant):
    # import pdb; pdb.set_trace()
    response = client.post("/account/login/", dict(email = "subhnesh0@gmail.com", password = "subh@2310"))
    token = response.data['access']
    payload= dict(
        name = "Pizza", merchant=add_merchant.id, cost=600
    ) 
    response=client.post("/account/items/", payload, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert response.status_code == 201

@pytest.mark.django_db
def test_store_creation_api_endpoint(user, add_merchant, add_item):
    # import pdb; pdb.set_trace()
    response = client.post("/account/login/", dict(email = "subhnesh0@gmail.com", password = "subh@2310"))
    token = response.data['access']
    req_send = client.post("/account/stores/", dict(name = "Bellandur Kfc Shop", address = "bellandur green glen layout", lat = 13, lng = 13, merchant = add_merchant.id, items=add_item.id), **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201

@pytest.mark.django_db
def test_order_creation_api_endpoint(user, add_merchant, add_store,  add_item,):
    # import pdb; pdb.set_trace()
    response = client.post("/account/login/", dict(email = "subhnesh0@gmail.com", password = "subh@2310"))
    token = response.data['access']
    req_send = client.post("/account/orders/", dict(merchant=add_merchant.id, items =add_item.id, store = add_store.id, total_cost=600), **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert req_send.status_code == 201