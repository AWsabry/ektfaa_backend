from django.urls import path
from Register_Login import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'Register_Login'

urlpatterns = [
    path('', views.index, name='index'),
    # APIs URL
    path('get_csrf_token_api/',view = views.get_csrf_token_api.as_view(), name = "get_csrf_token_api"),
    path('create_users_API/', view= views.create_users_API.as_view(), name='create_users_API'),
    path('login_view/', view= views.LoginView, name='login_view'),
    path('get_user_by_email/<str:email>', view= views.get_user_by_email.as_view(), name='get_user_by_email'),
    path('get_active_users/', view= views.get_active_users.as_view(), name='get_active_users'),

    # Getting the tokens - No Views, REST TEMPLATE

    # This endpoints generates the token that should be added as a Bearer token, and this endpoint require the email and the password of the user to have the token for this user 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



