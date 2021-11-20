from django.urls import path, include
from rest_framework import routers
from .api_views import PostViewSet, WebsViewSet, UserLikesCount, \
    UserPostsCount, PostWeb, Tops, NotificationViewSet, SetInActive, ProfilePostsViewSet, \
    ProfileViewSet, IssueCreateAPI, WebsAddAPIView, OTPSystem

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, 'Post')
router.register(r'webs', WebsViewSet, 'Webs')
router.register(r'get-notifications', NotificationViewSet, 'get-notification')
router.register(r'profile-posts', ProfilePostsViewSet, 'profile-posts')
router.register(r'profile', ProfileViewSet, 'profile')


urlpatterns = [
    path('v2/', include('djoser.urls')),
    path('', include(router.urls)),
    path('me-like/', UserLikesCount.as_view(), name='user_likes'),
    path('me-count/', UserPostsCount.as_view(), name='user_posts'),
    path('webs-post/', PostWeb.as_view(), name='webs-post'),
    path('set-inactive/', SetInActive.as_view(), name='setInActive'),
    path('tops/', Tops.as_view(), name='tops'),
    path('issue/', IssueCreateAPI.as_view(), name='issue-api'),
    path('add-web/', WebsAddAPIView.as_view(), name='web-add-api'),
    path('otp/', OTPSystem.as_view(), name='otp-manager')
]