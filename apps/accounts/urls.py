from .views import profile
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    # Api

    # api
    path('', profile, name='profile'),
]
