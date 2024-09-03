from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('profile/<int:pk>/', views.userProfile, name='user_profile'),
    path('change-login/', views.change_login, name='change_login'),
    
    
    path('',  views.home, name='home'),
    path('group/<str:pk>/', views.group, name="group"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('participants/<str:pk>/', views.participants, name="participants"),
    path('profile/update/<int:pk>/', views.profile_view, name='update_profile'), 
    
    
    
    
    

    path("create-group/", views.createGroup, name="create-group"),
    path("update-group/<str:pk>/", views.updateGroup, name="update-group"),
    path("delete-group/<str:pk>/", views.deleteGroup, name="delete-group"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)