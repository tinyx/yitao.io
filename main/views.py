from django.contrib.auth.models import User
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


@api_view(["post"])
@permission_classes(
    [AllowAny,]
)
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user = User.objects.create_user(
            serialized.initial_data["username"],
            serialized.initial_data["email"],
            serialized.initial_data["password"],
        )

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({"token": token}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
