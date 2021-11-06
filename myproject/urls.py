"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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


from cat import views
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from myproject import settings

from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),  
    path('accounts/', include('django.contrib.auth.urls')),
    path('change_password/', auth_views.PasswordChangeView.as_view()), 
   
    # path('accounts/register/', views.registerPage),
    # path('accounts/login/', views.login, name='login'),

    path('cat/', include('cat.urls')),
    path('', RedirectView.as_view(url="cat/")), 
  
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

