from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from page import views as page_views
from posts.views import PostListView, WebPostListView, UserPostListView, PostDeleteView, PostCreateResponseView
from users import views as user_views
from django.contrib.auth import views as auth_views
from posts import views as posts_views
from webs import views as webs_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', page_views.home, name='home'),
    path('user-data-download/', user_views.download_user_data, name='user_data'),
    path('login/', user_views.login_request,name='login'),
    path('feed/', PostListView.as_view(), name='feed'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
    path('register/', user_views.register, name='register'),
    path('Website/<str:name>', WebPostListView.as_view(), name='web-posts'),
    path('user/<str:name>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateResponseView.as_view(), name='create_post'),
    path('post/on-website/new/<str:pk>',
         posts_views.createOnPost, name='create_post_onweb'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             html_email_template_name='users/password_reset_html_email.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('update-profile/', user_views.edit_profile, name='user-updating'),
    path('search/', webs_views.SearchWebsListView.as_view(), name='search'),
    path('add-web/', webs_views.add_web, name='add_web'),
    path('report-issue/', user_views.issue, name='issue'),
    path('report-issue/<int:id>', posts_views.report_post, name='report_post'),
    path('posts/<int:id>/', webs_views.posts_like, name='posts_like'),
    path('feed/post/itemDel<int:id>/',
         posts_views.delete_post, name='post-delete'),
    path('Website/post/itemDel<int:id>/',
         posts_views.delete_post, name='post-delete-2'),
    path('download-user-data-posts/',
         user_views.export_posts, name='download-data-posts'),
    path('download-user-data-issues/',
         user_views.export_issues, name='download-data-issues'),
    path('download-user-data-user/',
         user_views.export_user, name='download-data-user'),
    path('paytm/', include('paytm.urls')),
    path('count-posts/', page_views.send_count),
    path('votp/',user_views.otp_ck, name='otp_ck'),
    path('votp2/',user_views.otp_ck_2, name='otp_ck_2'),
    path('resend_otp/',user_views.resend_otp, name='resend_otp'),
    path('change_number/',user_views.change_number, name='change_number'),
    path('disable_account/',user_views.disable_account, name='disable_account'),
    path('api/', include('rest.urls')),
    path('auth/', include('users.urls'))
   ]

handler404 = page_views.handler404
handler500 = page_views.handler500


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
