from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include([
        path('', include('client_auth.urls')),
        path('', include('client_account.urls')),
        path('', include('client_source.urls')),
        path('', include('client_ticket.urls')),
        path('', include('client_category.urls')),
    ])),
    path('api/admin/', include([
        path('', include('admin_auth.urls')),
        path('', include('admin_user.urls')),
        path('', include('admin_ticket.urls'))
    ]))
]
