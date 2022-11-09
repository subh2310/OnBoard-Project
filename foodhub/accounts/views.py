import structlog
from .serializers import *
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import create_store, create_order
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse_lazy
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import MerchantPermission, ConsumerPermission
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = structlog.get_logger(__name__)
log = logger.new()
logger_name = str(logger).upper()


def return_role(user):
    p = Profile.objects.get(user=user)
    if p.role == 1:
        role = "Merchant"
    elif p.role == 2:
        role = "Customer"
    return role


@api_view(['GET'])
def ApiHomepage(request, format=None):
    log.info(event = "{} tries to access Home Page".format(request.user), user = request.user)
    # log.info("Home Page", bar = "buzz")
    return Response({
        'Register': reverse_lazy('register', request=request, format=format),
        'Login': reverse_lazy('login', request=request, format=format),
        'Stores': reverse_lazy('stores', request=request, format=format),
        'Items': reverse_lazy('items', request=request, format=format),
        'View Consumers': reverse_lazy('view-consumer', request=request, format=format),
        'View Orders': reverse_lazy('seeorders', request=request, format=format),
        'Place Orders': reverse_lazy('placeorders', request=request, format=format),
        'Change Password': reverse_lazy('change-password', request=request, format=format)
    })


class UserRegisterView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED
            username = request.data['username']
            password = request.data['password']
            email = request.data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }
            log.info("{} with {} email and {} role register.".format(username, email, return_role(user)), user = username)
            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            pk = User.objects.get(username=serializer.data['username']).pk
            role = Profile.objects.get(user=pk).role
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                    'role': role
                }
            }
            log.info("{} with {} role successfully login.".format(username, return_role(user)), user = request.user)
            return Response(response, status=status_code)


class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                log.warning("{} with {} role not able to changed their password.".format(
                self.request.user, return_role(self.request.user)), user = request.user)
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }
            log.info("{} with {} role successfully changed their password.".format(
                self.request.user, return_role(self.request.user)), user = self.request.user.username)
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoresView(generics.ListCreateAPIView):
    serializer_class = StoresSerializer
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MerchantPermission)

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        stores = Stores.objects.filter(merchant=profile)
        if stores:
            log.info("{} has accessed their stores list.".format(self.request.user.username), user = self.request.user.username)
        else:
            log.info("{} don't have any stores".format(self.request.user.username), user = self.request.user.username)
        return stores

    def perform_create(self, serializer):
        pk = self.request.user.pk
        create_store.delay(user=pk, data=serializer.data)
        log.info("{} have added a new store.".format(self.request.user.username), user = self.request.user.username)


class ItemsView(generics.ListCreateAPIView):
    serializer_class = ItemSerializers
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MerchantPermission)

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        items = Items.objects.filter(stores__merchant=profile)
        if items:
            log.info("{} has accessed their stores's item list.".format(self.request.user.username), user = self.request.user.username)
        else:
            log.info("{} don't have any items in their stores".format(self.request.user.username))
        return items

    def perform_create(self, serializer):
        serializer.save()
        log.info("{} merchant have added a new item in their store.".format(self.request.user.username), user = self.request.user.username)

class PlaceOrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, ConsumerPermission)

    def get_queryset(self):
        orders = Orders.objects.filter(user=self.request.user)
        if orders:
            log.info("{} have accessed their order's list.".format(self.request.user.username), user = self.request.user.username)
        else:
            log.info("{} have not placed any order yet.".format(self.request.user.username), user = self.request.user.username)
        return orders

    def perform_create(self, serializer):
        pk = self.request.user.pk
        create_order.delay(user=pk, data=serializer.data)
        log.info("{} have placed a new order.".format(self.request.user.username), user = self.request.user.username)


class SeeOrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MerchantPermission)

    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        orders = Orders.objects.filter(merchant=profile)
        if orders:
            log.info("{} have accessed their order's list.".format(self.request.user.username), user = self.request.user.username)
        else:
            log.info("{} don't have any order placed yet.".format(self.request.user.username), user = self.request.user.username)
        return orders


class ViewConsumerView(generics.ListAPIView):
    serializer_class = ViewConsumerSerializer
    authentication_class = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, MerchantPermission)

    def get_queryset(self):
        user = User.objects.filter(profile__role=2)
        log.info("{} have accessed the registered consumer list".format(self.request.user.username), user = self.request.user.username)
        return user
