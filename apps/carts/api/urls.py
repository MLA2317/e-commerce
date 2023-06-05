from django.urls import path
from . import views


urlpatterns = [
    path('wishlist/list-create/', views.WishListListCreateAPIView.as_view()),
    path('add-cart/', views.AddToCartCreateApi.as_view()),
    path('my-cart/', views.MyCartListApi.as_view()),
    path('my-cart/<int:pk>/', views.DeleteFromMyCart.as_view()),
    path('order/', views.OrderAPIView.as_view())
]
