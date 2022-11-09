from django.urls import path
from rest_framework import routers
from .views import *

# router = routers.DefaultRouter()
# router.register('items', ItemsView, 'items')

urlpatterns = [
    path("", ApiHomepage),
    path("register/", UserRegisterView.as_view(), name = 'register'),
    path("login/", AuthUserLoginView.as_view(), name = 'login'),
    path("stores/", StoresView.as_view(), name = "stores"),
    path("place_orders/", PlaceOrderView.as_view(), name = "placeorders"),
    path("see_orders/", SeeOrderView.as_view(), name = "seeorders"),
    path("change-password/",UserChangePasswordView.as_view(), name = "change-password"),
    path("view-consumer/", ViewConsumerView.as_view(), name = "view-consumer"),
    path("items/", ItemsView.as_view(), name = "items")
]

# urlpatterns += router.urls
