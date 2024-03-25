from django.contrib import admin
from django.urls import path, include

handler404 = 'pages.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('', include('library.urls'))
]
