from django.urls import path
from .views import register_api, login_api, logout_api

urlpatterns = [
    path('register/', register_api),
    path('login/', login_api),
    path('logout/', logout_api),
]
