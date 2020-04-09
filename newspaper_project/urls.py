"""newspaper_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView
from articles import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
urlpatterns = [
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change-password.html',
            success_url = reverse_lazy('article_list')
        ),
        name='change_password'
    ),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), 
    path('users/', include('django.contrib.auth.urls')),
    url(r'^login/$',LoginView.as_view(), name='login'),
    #url(r'^logout/$', LogoutView.as_view(), name='logout'), 
    path('articles/', include('articles.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('', include('pages.urls')),  
    #url(r'^settings/$', views.settings, name='settings'),
    #url(r'^settings/password/$', views.password, name='password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

