from django.contrib import admin
from django.urls import path, include
from ShortenYourLinkDjangoRest.swagger import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ShortenYourLink-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    path('ShortenYourLink/', include('api.urls')),
]

urlpatterns += doc_urls
