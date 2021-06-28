from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login, name='login'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem , name='update_item'),
    path('',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]