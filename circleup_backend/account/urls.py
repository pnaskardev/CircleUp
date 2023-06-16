from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('editprofile/', api.edit_profile, name='edit_profile'),
    path('friends/request/', api.send_friend_request, name='send_friend_request'),
    path('friends/handle/', api.handle_request, name='handle_request'),
    path('friends/', api.friends, name='friends'),
]
