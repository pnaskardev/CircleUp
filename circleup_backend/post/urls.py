from django.urls import include, path

from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:pk>/like/', api.post_like, name='post_list'),
    path('profile/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
]
