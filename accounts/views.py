from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    user = authenticate(username=username, password=password)
    if not user:
        return Response(status='401')
    token, created = Token.objects.get_or_create(user=user)
    return Response(data={"token": token.key})