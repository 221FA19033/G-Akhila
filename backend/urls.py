from django.contrib import admin
from django.urls import path, include
from shop.views import login_view, signup_view, logout_view, home_redirect
from django.conf import settings
from django.conf.urls.static import static
from shop import urls as shop_urls  # import the app urls.py module

urlpatterns = [
    path('', home_redirect, name='home'),        # root URL → login check
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('products/', include('shop.urls')),     # web pages
    path('api/', include((shop_urls.api_urlpatterns, 'shop'), namespace='api')),  # API endpoints
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
