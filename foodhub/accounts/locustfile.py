# from pos.models import models
from locust import HttpUser, task, between
# from django.contrib.auth.models import User

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    token = ""
    username = ""

    @task
    def view_stores(self):
        response = self.client.get("stores/",
            headers={"Authorization": "Bearer " + self.token},
        )

    # @task
    # def add_stores(self):
    #     user = User.objects.get(username = self.username)
    #     profile = models.Profile.objects.get(user = user)
    #     data = {"name" : "WhiteField Outlet", "address" : "WhiteField", "lat" : "13", "lng" : "13", "merchant" : "merchant_data"}
    #     self.client.post("stores/", data, headers={"Authorization": "Bearer " + self.token})

    @task
    def view_items(self):
        response = self.client.get("items/",
            headers={"Authorization": "Bearer " + self.token},
        )

    @task
    def see_orders(self):
        response = self.client.get("see_orders/",
            headers={"Authorization": "Bearer " + self.token},
        )

    def on_start(self):
        response = self.client.post("login/", {"username" : "mcd", "password" : "mcd"})
        response = response.json()
        self.token = response['access']
        self.username = response["authenticatedUser"]["username"]
