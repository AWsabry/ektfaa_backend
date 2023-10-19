
from django.urls import reverse
from django.db import models






class Category(models.Model):
    Category_name = models.CharField(max_length=250,unique = True,)
    display_name =  models.CharField(max_length=250, blank=True,null = True)
    categoryslug = models.SlugField(unique=True, db_index=True,blank=True,null = True)
    image = models.ImageField(
        upload_to="Categories", blank=True,null = True )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.Category_name)
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url_category(self):
        return reverse('categories_and_products:category_details', args=[self.Restaurant.restaurant_slug] + [self.categoryslug])

    class Meta:
        verbose_name_plural = "Categories"

def upload_product_images(instance, filename):
    return 'CloudKitchen/%s/%s' % (instance.name, filename)
 
Medical_Questions = (
        ("Restaurant", "Restaurant"),
        ("Cloud Kitchen", "Cloud Kitchen"),)


class Product(models.Model):
    name = models.CharField(max_length=250, blank=True)
    ArabicName = models.CharField(max_length = 250, blank = True, null= True)
    productslug = models.SlugField(unique=True, db_index=True,)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0)
    image =  models.ImageField(
        upload_to=upload_product_images, blank=True,null = True )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null = True,)
    boughtPrice = models.FloatField(blank=True, null=True, default=0)
    offerPercentage = models.FloatField(blank=True, null=True,)
    active = models.BooleanField(default=True)
    Most_Popular = models.BooleanField(default=False)
    New_Products = models.BooleanField(default=False)
    Best_Offer = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    limit = models.IntegerField(default= 0, blank = True, null = True)

    def __str__(self):
        arabic_string = self.ArabicName
        arabic_string.encode('unicode-escape')
        return arabic_string
    


    def discountpercentage(self):
        if self.boughtPrice:
            discountAmount = self.boughtPrice - self.price
            self.offPercentage = (discountAmount/self.oldPrice) * 100
            return (int(self.offPercentage))
        else:
            pass
    offerPercentage = property(discountpercentage)
