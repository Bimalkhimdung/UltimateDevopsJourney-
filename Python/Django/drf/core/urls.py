from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('user/',views.user, name='Users'),
    path('legal-info/',views.legal_info, name='Legal info')
]
