from .views import profile
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('', profile, name='profile'),
]
