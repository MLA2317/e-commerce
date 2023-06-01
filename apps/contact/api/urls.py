from django.urls import path
from . import views


urlpatterns = [
    path('list-create/', views.ContactCreateView.as_view())
]
