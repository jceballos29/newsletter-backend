from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from accounts.serializers import UserRegisterSerializer, UserSerializer


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=(AllowAny, ))
def register(request):
    user_serialized = UserRegisterSerializer(data=request.data)
    user_serialized.is_valid(raise_exception=True)
    user = user_serialized.save()

    return Response(
        status=status.HTTP_201_CREATED,
        data=UserSerializer(user).data
    )

