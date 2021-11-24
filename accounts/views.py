from datetime import datetime, timedelta

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from accounts.serializers import UserRegisterSerializer, UserSerializer
from accounts.tasks import send_email_registration


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=(AllowAny, ))
def register(request):
    user_serialized = UserRegisterSerializer(data=request.data)
    user_serialized.is_valid(raise_exception=True)
    user = user_serialized.save()

    print(user.username, user.email, user.first_name)
    send_email_datetime = datetime.now() + timedelta(seconds=30)
    send_email_registration.apply_async(
        args=[user.username, user.email, user.first_name],
        eta=send_email_datetime
    )

    return Response(
        status=status.HTTP_201_CREATED,
        data=UserSerializer(user).data
    )

