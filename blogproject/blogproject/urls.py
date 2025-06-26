from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),  # Tu app principal
    path('', include('django.contrib.auth.urls')),  # Login/Logout
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # ✅ Endpoints OAuth2
]
