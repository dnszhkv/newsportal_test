from django.urls import path
from .views import IndexView, upgrade_me

urlpatterns = [
    path('', IndexView.as_view(), name='account_info'),
    path('upgrade/', upgrade_me, name='upgrade')
]
