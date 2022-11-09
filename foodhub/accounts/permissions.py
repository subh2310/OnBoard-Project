import structlog
from .models import Profile
from rest_framework import permissions

logger = structlog.get_logger(__name__)
log = logger.new()
logger_name = str(logger).upper()


class MerchantPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        if p.role == 2:
            log.warning(logger_name + ": " + '{} was trying to access something which requires Merchant '
                        'Permission'.format(user.username))
        return user and p.role == 1

class ConsumerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        p = Profile.objects.get(user=user)
        if p.role == 1:
            log.warning(logger_name + ": " + '{} was trying to access something which requires Consumer '
                        'Permission'.format(user.username))
        return user and p.role == 2
