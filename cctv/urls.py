from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('counts/<str:pk>', views.Getcounts),
    path('markers/<str:pk1>/<str:pk2>', views.Getmapparameter),
]