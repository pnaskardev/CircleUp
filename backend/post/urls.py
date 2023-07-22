from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='post-list'),
    path('create/', views.Posts.as_view({'post': 'create'}), name='post-create'),
    path('profile/<str:id>/', views.Posts.as_view({'get': 'list'}), name='post-create'),
]
