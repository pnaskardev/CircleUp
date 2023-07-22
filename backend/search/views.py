from django.shortcuts import render
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny
from account.models import User
from account.serializers import UserSerializer


class AccountAPIView(generics.ListCreateAPIView):
    permission_classes=[AllowAny]
    search_fields = ['username']
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserSerializer