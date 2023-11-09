from itertools import count
from django.contrib.auth import authenticate, login as user_login
from django.shortcuts import render
from django.utils.translation import gettext as _
# Rest Libraries
from rest_framework.response import Response
from rest_framework import status
from django.utils import translation
from rest_framework.views import APIView
from django.db.models import Q
import requests

# Importing the utilts file


# from cart_and_orders.models import Cart
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import Product,Category, UserUpload,SubCategory,Company,Sector,Tags
from .serializers import ProductsSerializer, SubCategorySerializer, UserUploadSerializer
from urllib.parse import unquote
from Register_Login.models import Profile
import re

def index_category(request):
    return render(request, "category.html")



class GetSearchedProducts(APIView):
    def get(self, request, phone, searched):
        if not searched:
            return Response({"message": "Please provide a search query"}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = Profile.objects.get(PhoneNumber=phone,)
        except ObjectDoesNotExist:
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned:
            return Response({"message": "Multiple profiles found for the given phone number"}, status=status.HTTP_400_BAD_REQUEST)
        

        decoded_user_input = unquote(searched)
        
        pattern = r'\b{}\b'

        arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+'

        is_arabic = bool(re.search(arabic_pattern, decoded_user_input))

        if is_arabic:
            search_pattern = pattern.format(re.escape(decoded_user_input))
            search_pattern = r'(?i)' + search_pattern
        else:
            search_pattern = pattern.format(re.escape(decoded_user_input))
            search_pattern = r'(?i)' + search_pattern


        # Get products matching the search in English or Arabic names with avoid=False and the user's country
        not_avoided_english_results = Product.objects.filter(Q(avoid=False, product_english_name__iregex=search_pattern, country_of_existence=user.Country) | Q(tag__english_name__iregex = search_pattern))
        not_avoided_arabic_results = Product.objects.filter(Q(avoid=False, product_arabic_name__iregex=search_pattern, country_of_existence=user.Country) | Q(tag__arabic_name__iregex = search_pattern)) 

        company_english = Product.objects.filter(Q(avoid=True, company__englishName__iregex=search_pattern, country_of_existence=user.Country) | Q(tag__english_name__iregex = search_pattern))
        company_arabic = Product.objects.filter(Q(avoid=True, company__arabicName__iregex=search_pattern, country_of_existence=user.Country) | Q(tag__arabic_name__iregex = search_pattern))

        # Combine the English and Arabic results using OR
        products = not_avoided_english_results | not_avoided_arabic_results | company_english | company_arabic

        # Check if products exist based on the search
        if products.exists():
            serializer = ProductsSerializer(products, many=True)
            response_data = {"Names": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        
        else:
            # Find products in the same category with avoid=False and in the user's country
            sub_category = Product.objects.filter(avoid=True, product_english_name__iregex=search_pattern, country_of_existence=user.Country).values('sub_category').first()
            sub_category_arabic = Product.objects.filter(avoid=True, product_arabic_name__iregex=search_pattern, country_of_existence=user.Country).values('sub_category').first()

            if sub_category:
                related_products = Product.objects.filter(avoid=False, sub_category=sub_category['sub_category'], country_of_existence=user.Country)
                if related_products.exists():
                    serializer = ProductsSerializer(related_products, many=True)
                    response_data = {"Names": serializer.data}
                    return Response(response_data, status=status.HTTP_200_OK)
                else:

                    return Response({"message": "No local products found in the same Sub-category"}, status=status.HTTP_302_FOUND)
               
            elif sub_category_arabic:
                print("Arabic")
                related_products_arabic = Product.objects.filter(avoid=False, sub_category=sub_category_arabic['sub_category'], country_of_existence=user.Country)
                if related_products_arabic.exists():
                    serializer_arabic = ProductsSerializer(related_products_arabic, many=True)
                    response_data_arabic = {"Names": serializer_arabic.data}
                    return Response(response_data_arabic, status=status.HTTP_200_OK)
                else:                
                    return Response({"message": "No local products found in the same Arabic Sub-category"}, status=status.HTTP_302_FOUND)
            else:
                return Response({"message": "No local products found"}, status=status.HTTP_302_FOUND)

    

class UserUploadsProducts(APIView):
    def post(self, request,*args, **kwargs):
        serializer = UserUploadSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Added To Cart", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user_uploads = UserUpload.objects.all()
        serializer = UserUploadSerializer(user_uploads, many=True)
        response = {"Names": serializer.data}
        return Response(response,status=status.HTTP_200_OK)



class SubCategoryView(APIView):    
    def get(self, request):
        subCategory = SubCategory.objects.all()
        serializer = SubCategorySerializer(subCategory, many=True)
        response = {"Names": serializer.data}
        return Response(response,status=status.HTTP_200_OK)


