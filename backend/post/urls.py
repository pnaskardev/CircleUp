from django.urls import path

from . import views

urlpatterns = [
    path('', views.Posts.as_view({'get': 'list'}), name='post-list'),
    path('<uuid:pk>/like/',views.post_like, name='post-like'),
    path(
        'create/', views.Posts.as_view({'post': 'create'}), name='post-create'),
    path('profile/<str:id>/', views.UserPosts.as_view(), name='post-create'),
]
