
from django.urls import reverse
from django.db import models
from nltk.stem import PorterStemmer
from django.db.models import Q

stemmer = PorterStemmer()



class Company(models.Model):
    englishName = models.CharField(max_length=100,blank=True,null=True)
    arabicName = models.CharField(max_length=100,blank=True,null=True)
    number_of_registration = models.CharField(max_length=250,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    district = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to="Companies", blank=True,null = True )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.englishName)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Companies"

class Sector(models.Model):
    englishName = models.CharField(max_length=250,unique = True,)
    arabicName = models.CharField(max_length=250,unique = True,)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.englishName)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Sectors"

class Category(models.Model):
    Category_English_name = models.CharField(max_length=250,unique = True,)
    Category_Arabic_name = models.CharField(max_length=250,unique = True,)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE,blank=True,null = True,)
    categoryslug = models.SlugField(unique=True, db_index=True,blank=True,null = True)
    image = models.ImageField(
        upload_to="Categories", blank=True,null = True )
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.Category_English_name)
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    Sub_Category_English_name = models.CharField(max_length=250,unique = True,blank=True,null = True,)
    Sub_Category_Arabic_name = models.CharField(max_length=250,blank=True,null = True,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null = True,)
    image = models.ImageField(
        upload_to="Sub-Category", blank=True,null = True )
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.Sub_Category_English_name)
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Sub-Categories"

class Product(models.Model):
    product_english_name = models.CharField(max_length = 250, blank = True, null= True)
    product_arabic_name = models.CharField(max_length = 250, blank = True, null= True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,blank=True,null = True,)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,blank=True,null = True,)
    country_of_manufacturing = models.CharField(max_length = 250, blank = True, null= True)
    country_of_existence = models.CharField(max_length = 250, blank = True, null= True)
    importer_name = models.CharField(max_length = 250, blank = True, null= True)
    franchise = models.BooleanField(default=False)
    range_of_prices = models.CharField(max_length = 250, blank = True, null= True)
    year_of_import = models.CharField(max_length = 250, blank = True, null= True)
    created = models.DateTimeField(auto_now_add=True)
    productslug = models.SlugField(unique=True, db_index=True,blank=True,null = True)
    description = models.TextField(blank=True,null=True)
    avoid = models.BooleanField(default=True)

    def __str__(self):
        arabic_string = self.product_arabic_name
        arabic_string.encode('unicode-escape')
        return arabic_string


