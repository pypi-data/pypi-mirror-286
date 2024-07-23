from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from milea_notify.models import Notification


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def mark_as_read(request, notification_id):
    """ Set the notification status to -is_read- """
    notification = get_object_or_404(Notification, pk=notification_id)
    if request.user == notification.user:
        notification.is_read = True
        notification.save()
        return Response({}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_403_FORBIDDEN)
