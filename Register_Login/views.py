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
from Register_Login.models import Profile
from Register_Login.serializers import LoginSerializer, UserSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
# Importing the utilts file

# getting csrf token
from django.middleware.csrf import get_token

# Importing Models

# from cart_and_orders.models import Cart
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes



# Get CSRF Token
class get_csrf_token_api(APIView):
    def get(self,request):
        token = csrf_token = get_token(request)
        return JsonResponse({"token": token}, safe=False)
    


class create_users_API(APIView):
    def post(self,request,):
        serializer = UserSerializer(data= request.data,)
        if serializer.is_valid():
            user = Profile.objects.create_user(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    password=request.data['password'],
                    city=request.data['city'],
                    PhoneNumber=request.data['PhoneNumber'],
                    Country=request.data['Country'],
                    age = request.data['age'], 
                    gender = request.data['gender'],
                    is_active = True,
                    # Location = Location.objects.get(id = request.data['Location'])
                )
            if user:
                return Response("User Created Successfully", status = status.HTTP_200_OK)
            else:
                return Response("Error Creating User", status = status.HTTP_403_FORBIDDEN)
        else:
            return Response("Serializer Not Valid", status = status.HTTP_403_FORBIDDEN)

# Get All Users
class get_active_users(APIView):
    def get(self,request):
        all = Profile.objects.filter(is_active = True)
        serializer = UserSerializer(all,many = True)
        return JsonResponse({"Names": serializer.data}, safe=False)


# Login
class Login_users_API(APIView):
    def post(self,request,):
        serializer = LoginSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    update_last_login(None, user)
                    user_login(request, user)
                    return Response({"message": "Login successful","Names" : serializer.data,"code":status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "User account is not active","code":status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"message": "Invalid credentials","code":status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


# Get User by Id
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class get_user_by_email(APIView):
    def get(self,request,email,*args, **kwargs):
        all = Profile.objects.filter(is_active = True,email=email)
        serializer = UserSerializer(all,many = True)
        return JsonResponse({"Names": serializer.data}, safe=True,status = status.HTTP_200_OK)
    
    def post(self,request,email,*args, **kwargs):
        all = Profile.objects.filter(is_active = True,email=email)
        exist = Profile.objects.filter(is_active = True,email=email).exists()
        serializer = UserSerializer(all,many = True)
        return JsonResponse({"Names": serializer.data, "exist":exist}, safe=True,status = status.HTTP_403_FORBIDDEN)
    

class get_user_by_phone(APIView):
    def get(self,request,phone,*args, **kwargs):
        all = Profile.objects.filter(is_active = True,PhoneNumber=phone)
        serializer = UserSerializer(all,many = True)
        return JsonResponse({"Names": serializer.data}, safe=True,status = status.HTTP_200_OK)


class UpdateUserCountry(APIView):
    def post(self, request, phone):
        updated_country = request.data.get('updated_country')  # Assuming the updated country is sent in the request data
        if not updated_country:
            return JsonResponse({"message": "Please provide the updated country"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the user's profile
            user_profile = Profile.objects.get(is_active=True, PhoneNumber=phone)

            # Update the user's country
            user_profile.Country = updated_country
            user_profile.save()
            # Serialize the updated user profile
            serializer = UserSerializer(user_profile)

            return JsonResponse({"message": "Country Updated"}, safe=True, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return JsonResponse({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"message": "An error occurred while updating the country"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
def index(request):
    return render(request, "index.html")