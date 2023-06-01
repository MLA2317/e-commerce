from django.urls import path
from . import views


urlpatterns = [
    path('tag/list/', views.TagListView.as_view()),
    path('tag/create/', views.TagCreateView.as_view()),
    path('tag/rud/<int:pk>/', views.TagRUDView.as_view()),

    path('post/list/', views.PostListView.as_view()),
    path('post/create/', views.PostCreateView.as_view()),
    path('post/rud/<int:pk>/', views.PostRUDView.as_view())
]
