
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductDetail
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views



app_name= 'ebookstore'
urlpatterns = [
    #path('',ProductList.as_view(),name='homepage1'),
    path('complain/',views.complain,name='complain'),
    path('', views.display_category, name='displaycategory'),
    path('stores/', views.display_stores, name='displaystores'),
    path('category/<int:id>', views.display_percategory, name='display_percategory'),
    path('store/<int:id>', views.display_perstores, name='display_perstore'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product_detail'), 
    path('cart/', views.carthome, name='carthome'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
    path('signup/', views.signup_view,name='register'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('profile/', views.profile,name='userprofile'),
    path('editprofile/', views.edit_profile,name='edituserprofile'),
    path('confirmcomplain/', views.confirmcomplain, name='confirmcomplain'),
    path('addcomment/<int:id>', views.add_comment, name='addcomment'),
    path('like/',views.like_products,name='like_products'),
    path('favourites/<int:id>', views.favourite_products,name='favourite_products'),
    path('favouriteproducts/', views.userfavourite_products,name='userfavourite_products'),
    url(r'^changepassword/$', views.change_password, name='change_password'),
    path('Salesrequest/', views.Salesrequest, name='Salesrequest'),
    path('confirmsalesrequest/', views.confirmsalesrequest, name='confirmsalesrequest'),

    
   
    path('checkout/', views.checkout, name='checkout'),
    path('confirmorder/', views.confirmorder,name='confirmorder'),
     

]



urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)