from rest_framework import serializers
from categories_and_products.models import Category, Product,Company,Tags

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, allow_null = True)
    class Meta:
        model = Product
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'






