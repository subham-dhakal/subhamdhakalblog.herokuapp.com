
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSiteMap
from blog import views

sitemaps = {
    'posts':PostSiteMap,
}

urlpatterns = [
    path('', views.home ,name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace = 'blog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name= 'django.contrib.sitemaps.views.sitemap')  # sitemaps
]
