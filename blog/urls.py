from django.contrib import admin
from django.urls import path, include
from .import views
from .feeds import LatestPostsFeed   # RSS Feed


app_name = 'blog'


urlpatterns = [
    path('', views.post_list, name='post_list'), # url for FBV post_list
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name= 'post_feed'),                 # RSS Feed URL
    path('search/', views.post_search, name='post_search')
]