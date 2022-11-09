from urllib import response
from .models import *
from celery import Celery
from .serializers import *
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task()
def create_store(user, data):
    user = User.objects.get(pk = user)
    profile = Profile.objects.get(user = user)
    serializer = StoresSerializer(data = data)
    valid = serializer.is_valid(raise_exception = True)
    if valid:
        serializer.save(merchant = profile)
        return valid
    else:
        response = {
            'success' : True,
            'status_code' : status.HTTP_400_BAD_REQUEST,
            'message' : "Error in Store Creation"
        }
        return Response(response, status = status.HTTP_400_BAD_REQUEST)


# def create_order(user, data):
#     user = User.objects.get(pk = user)
#     serializer = ItemSerializers(data = data)
#     valid = serializer.is_valid(raise_exception = True)
#     if valid:
#         serializer.save(user = user)
#         return valid
#     else:
#         response = {
#             'success' : True,
#             'status_code' : status.HTTP_400_BAD_REQUEST,
#             'message' : "Error in Order Creation"
#         }
#         return Response(response, status = status.HTTP_400_BAD_REQUEST)
@app.task()
def create_order(user, data):
    user = User.objects.get(pk=user)
    serializer = OrderSerializer(data=data)
    valid = serializer.is_valid(raise_exception=True)
    if valid:
        serializer.save(user=user)
        return valid
    else:
        response = {
            'success': True,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': "Error in Order Creation"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


