from django.contrib.auth import authenticate, login as user_login
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.models import update_last_login
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
# Rest Libraries
from rest_framework.response import Response
from rest_framework import status
from Register_Login.serializers import LoginSerializer, UserSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
# Importing the utilts file

# getting csrf token
from django.middleware.csrf import get_token

# Importing Models
from Register_Login.models import Profile

# from cart_and_orders.models import Cart
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes




def index_category(request):
    return render(request, "category.html")