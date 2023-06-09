from django.urls import include, path

from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('<uuid:pk>/like/', api.post_like, name='post_list'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('profile/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
]
