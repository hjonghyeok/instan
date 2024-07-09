from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page),
    path('register/', views.register_page),
    path('', views.main_page),
    path('logout/', views.logout, name='logout'),
]
