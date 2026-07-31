from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('menu/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('popular/', views.popular, name='popular'),
    path("product/<int:product_id>/", views.product_details, name="product_details"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('favorites/', views.favorites, name='favorites'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]