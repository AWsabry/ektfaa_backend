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
from .models import Product,Category
from .serializers import ProductsSerializer




def index_category(request):
    return render(request, "category.html")



class GetSearchedProducts(APIView):
    def get(self, request, searched):
        if not searched:
            return Response({"message": "Please provide a search query"}, status=status.HTTP_403_FORBIDDEN,)

        # Get products matching the search in English or Arabic names with avoid=False
        not_avoided_english_results = Product.objects.filter(avoid=False, product_english_name__icontains=searched)
        not_avoided_arabic_results = Product.objects.filter(avoid=False, product_arabic_name__icontains=searched)

        company_english = Product.objects.filter(avoid=True, company__englishName__icontains=searched)
        company_arabic = Product.objects.filter(avoid=True, company__arabicName__icontains=searched)


        # Combine the English and Arabic results using OR
        products = not_avoided_english_results | not_avoided_arabic_results
        company = company_english | company_arabic
       

        # Check if products exist based on the search


        if products.exists():
            serializer = ProductsSerializer(products, many=True)
            response_data = {"Names": serializer.data}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            category = Product.objects.filter(avoid=True, product_english_name__icontains=searched).values('category').first()
            if category:
                # Find products in the same category with avoid=False
                related_products = Product.objects.filter(avoid=False, category=category['category'])
                if related_products.exists():
                    serializer = ProductsSerializer(related_products, many=True)
                    response_data = {"Names": serializer.data}
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "No matching products found in the same category"}, status=status.HTTP_403_FORBIDDEN,)
            else:
                return Response({"message": "No matching products found"}, status=status.HTTP_403_FORBIDDEN)
    
            
