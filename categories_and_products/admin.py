from django.contrib import admin
from categories_and_products.models import Category, Product,Company, SubCategory,Sector,Tags
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.forms import CheckboxSelectMultiple
from django.db import models

class CompanyData(resources.ModelResource):
    class Meta:
        model = Company

class SectorData(resources.ModelResource):
    class Meta:
        model = Sector

class SubCategoryData(resources.ModelResource):
    class Meta:
        model = SubCategory

class CategoryData(resources.ModelResource):
    class Meta:
        model = Category

class ProductsData(resources.ModelResource):
    class Meta:
        model = Product


class CompanyAdmin(ImportExportModelAdmin):
    resources_classes = [CompanyData]
    list_display = ('englishName', 'arabicName', 'created','id')
    list_filter = ('created',)
    search_fields = ('englishName', 'arabicName',)

class SectorAdmin(ImportExportModelAdmin):
    resources_classes = [CompanyData]
    list_display = ('englishName', 'arabicName', 'created','id')
    list_filter = ('created',)
    search_fields = ('englishName', 'arabicName',)


class CategoryAdmin(ImportExportModelAdmin):
    resources_classes = [CategoryData]
    list_display = ('Category_English_name', 'Category_Arabic_name', 'sector', 'created','id')
    list_filter = ('created',)
    search_fields = ('Category_English_name', 'Category_Arabic_name', 'categoryslug')
    prepopulated_fields = {'categoryslug': ('Category_English_name',)}

class SubCategoryAdmin(ImportExportModelAdmin):
    resources_classes = [SubCategoryData]
    list_display = ('Sub_Category_English_name','Sub_Category_Arabic_name','category', 'created','id')
    list_filter = ('created',)
    search_fields = ('Sub_Category_English_name', 'Sub_Category_Arabic_name',)


class ProductAdmin(ImportExportModelAdmin):
    resources_classes = [ProductsData]
    list_display = ('product_english_name', 'product_arabic_name', 'sub_category', 'company', 'created')
    list_filter = ('created', 'sub_category', 'company')
    search_fields = ('product_english_name', 'product_arabic_name', 'sub_category__Sub_Category_English_name', 'company__englishName')
    prepopulated_fields = {'productslug': ('product_english_name',)}
    autocomplete_fields = ['sub_category','company']
    formfield_overrides = {
        models.ManyToManyField : {'widget' : CheckboxSelectMultiple},
    }



class TagsAdmin(admin.ModelAdmin):
    list_display = ('english_name')


admin.site.register(Sector,SectorAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Tags,)
