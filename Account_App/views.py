from business.models import Cuisine  
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from .models import Account
from .serializers import AccountSerializer, UserSerializer, BusinessAccountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from account.serializers import UserSerializer
from business.serializers import BusinessAccountSerializer

class UserAccountUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_user:
            serializer = UserSerializer(user.user_profile)
            return render(request, 'update_account.html', {'serializer': serializer, 'user': user})
        else:
            return Response({'detail': 'User account required for this view.'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        data = request.data

        if user.is_user:
            serializer = UserSerializer(user.user_profile, data=data, partial=True)
        else:
            return Response({'detail': 'User account required for this view.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return redirect('account-update')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BusinessAccountUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_business:
            serializer = BusinessAccountSerializer(user.business_profile)
            return render(request, 'update_account.html', {'serializer': serializer, 'user': user})
        else:
            return Response({'detail': 'Business account required for this view.'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        data = request.data

        if user.is_business:
            # Check if 'cuisine_ids' are present in the request data
            if 'cuisine_ids' in data:
                business_profile = user.business_profile
                cuisines = Cuisine.objects.filter(pk__in=data['cuisine_ids'])
                business_profile.cuisines.set(cuisines)
                business_profile.save()
                return redirect('account-update')

            # Continue with the existing behavior for updating other fields
            serializer = BusinessAccountSerializer(user.business_profile, data=data, partial=True)
        else:
            return Response({'detail': 'Business account required for this view.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return redirect('account-update')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AccountLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = Account.objects.get(username=username)
        if user.check_password(password):
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class AccountLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
