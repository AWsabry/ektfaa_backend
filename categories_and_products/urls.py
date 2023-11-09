from django.urls import path
from categories_and_products import views




app_name = 'categories_and_products'


urlpatterns = [

    # APIs URL
    path('category/', view=views.index_category, name='category'),
    path('get_products/<str:phone>/<str:searched>/', view= views.GetSearchedProducts.as_view(), name='get_products'),
    path('user_uploads/', view= views.UserUploadsProducts.as_view(), name='user_uploads'),
    path('sub_category/', view= views.SubCategoryView.as_view(), name='sub_category'),
]
