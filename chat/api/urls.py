from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('groups/', views.getGroups),
    path('groups/<str:pk>/', views.getGroup),
]