from django.urls import path

from .views import *


app_name = 'main'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('new_post', CreatePost.as_view(), name='new_post'),
    path('show_post/<slug:post_slug>', PostDetailView.as_view(), name='show_post'),
    path('login', LoginUser.as_view(), name = 'login'),
    path('logout', LogoutUser.as_view(), name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
    path('search', Search.as_view(), name='search'),
    path('about', About.as_view(), name='about'),
    path('user/<slug:user_slug>', UserPage.as_view(), name='user'),
    path('my_profile', MyProfile.as_view(), name='my_profile'),
    path('user_update/<int:user_pk>', ProfileUpdate.as_view(), name='profile_update'),
]
