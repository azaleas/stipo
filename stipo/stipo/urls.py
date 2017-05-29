"""stipo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import importlib
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from allauth.socialaccount import providers

from places.api.views import TwitterLogin

# http://bit.ly/2p87rHz - removing everything from allauth, except social

# twitter login - auth/twitter/login

providers_urlpatterns = []

for provider in providers.registry.get_list():
    prov_mod = importlib.import_module(provider.get_package() + '.urls')
    providers_urlpatterns += getattr(prov_mod, 'urlpatterns', [])

urlpatterns = [
    url(r'^api/v1/', include('places.api.urls', namespace='api')),
    url(r'^sa60_admin/', admin.site.urls),
    url(r'^auth/', include(providers_urlpatterns)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/twitter/$', TwitterLogin.as_view(), name='twitter_login'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
