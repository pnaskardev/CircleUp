from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.AccountAPIView.as_view(),name='account-search')
]
