import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from accounts.models import Merchant, Store, Order, Item
User=get_user_model()

client = APIClient()
@pytest.fixture
def user():
    payload= dict(
        password1="subh@2310",
        password2="subh@2310",
        email="subhnesh0@gmail.com",
        first_name="Subhnesh",
        last_name="Kumar"
    )
    client.post('/account/register/', payload)



@pytest.fixture
def add_merchant():
    merchant = Merchant.objects.create(
        name='Kfc',
        phone='9098786796',
        email="kfc@gmail.com",
    )
    return merchant

@pytest.fixture
def add_item(add_merchant):
    item = Item.objects.create(
        name="Pizza",
        cost=600,
        merchant=add_merchant,
        description="this is a Kfc shop",
    )
    return item
@pytest.fixture
def add_store(add_merchant, add_item):
    store = Store.objects.create(
        name='Bellandur kfc',
        address='Bellandur green glen layout',
        merchant=add_merchant,
        items=add_item
    )
    return store


@pytest.fixture
def add_order(add_merchant, add_item, add_store):
    order = Order.objects.create(
        merchant=add_merchant,
        store=add_store,
        items=add_item,
        total_cost=600  
    )
    return order



