from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.home , name='main-home'),
    #path('home/',views.home , name='main-home'),
    path('homepost',views.home_post , name='main-home-post'),
    path('register/',views.register , name='main-register'),
    path('signin/',views.signin , name='main-signin'),
    path('logout/',views.logout, name='main-logout'),
    path('cart/',views.cart, name='main-cart'),
    #path('cart/cart/',views.cart, name='main-cart'),
    path('OurTeam/',views.Team, name='main-team'),
    path('profile/',views.my_profile , name='main-profile'),
    path('checkout/',views.checkout, name='main-checkout'),
    path('signin/validation/', views.Email_validation, name='Email_validation'),
    path('register/validation1/', views.Email_validation, name='register_Email_validation'),
    path('success/',views.success , name='success'),
    path('search/',views.search , name='search'),
    path('searchpost/',views.search_post , name='main-search-post'),
]

