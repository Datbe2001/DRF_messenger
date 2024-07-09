from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from message_be.apps.message.views_container.user import UserDetailViewSet

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='login_api'),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('user/me/', UserDetailViewSet.as_view(), name='user-detail'),

]
