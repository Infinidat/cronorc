"""cronorc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from cronorc_server.main.views import home_view, job_view, edit_job_view, notify_view, hosts_view, host_view

admin.autodiscover()

urlpatterns = [
    path('', home_view, name='home'),
    path('jobs/<int:id>/', job_view, name='job'),
    path('jobs/<int:id>/edit', edit_job_view, name='edit_job'),
    path('hosts/', hosts_view, name='hosts'),
    path('hosts/<int:id>/', host_view, name='host'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('notify/', notify_view),
    path('admin/', admin.site.urls),
]
