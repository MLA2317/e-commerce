# from .views import profile
from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    # Api
    path('api/', include('accounts.api.urls'))

    # api
    # path('', profile, name='profile'),
]
