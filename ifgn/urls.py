"""
URL configuration for ifgn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ifgnapp import seo_files, error_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ifgnapp.urls')),
    path('manifest.json', seo_files.manifest_file),
    path('opensearch.xml', seo_files.open_search),
    path('robots.txt', seo_files.robot_file),
    path('feed.xml', seo_files.feed),
    path('sitemap.xml', seo_files.sitemap),
    path('blog-sitemap.xml', seo_files.post_sitemap),
]

handler404 = error_view.error_404
handler500 = error_view.error_500
handler403 = error_view.error_403
handler400 = error_view.error_400