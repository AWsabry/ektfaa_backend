from django.contrib import admin
from categories_and_products.models import Category, Product, SubCategory
from django.forms import CheckboxSelectMultiple
from django.db import models
# Register your models here.






class Categories_Admin(admin.ModelAdmin):
    prepopulated_fields = {'categoryslug': ('Category_name',), }
    list_filter = ("Category_name", "created",)
    list_display = ('Category_name', "created","active","id",)
    search_fields = ['Category_name']

    formfield_overrides = {
        models.ManyToManyField : {'widget' : CheckboxSelectMultiple},
    }

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        form.base_fields["image"].help_text = " * width: 700, height: 800px are recommended"
        return form


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'productslug': ('name','ArabicName',), }
    list_filter = ("category","created",)
    list_display = ('name', "price", "category",
                     "id", "created","Best_Offer", "Most_Popular","New_Products","active",)
    list_display_links = [
        'name',
        'category',
    ]
    search_fields = ['name']
    list_editable=['active']

    formfield_overrides = {
        models.ManyToManyField : {'widget' : CheckboxSelectMultiple},
    }














admin.site.register(Category, Categories_Admin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory)
