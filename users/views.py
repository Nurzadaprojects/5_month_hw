
import random
import string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .serializers import UserCreateSerializers, UserLoginSerializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


User = get_user_model()

@api_view(['POST'])
def registration_api_view(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = User.objects.create_user(username=username, password=password,
                                            is_active=False)

            confirmation_code = ''.join(random.choices(string.digits, k=6))

            user.confirmation_code = confirmation_code
            user.save()

            return Response({'message': 'User registered successfully',
                             'user_id': user.id},
                            status=status.HTTP_201_CREATED)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:

        return Response({'message': 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def confirm_api_view(request):
    if request.method == 'POST':
        confirmation_code = request.data.get('confirmation_code')

        user = User.objects.filter(confirmation_code=confirmation_code,
                                   is_active=False).first()

        if user:
            user.is_active = True
            user.save()

            return Response({'message': 'User confirmed successfully'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid confirmation code'},
                            status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserLoginSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid credentials'})



