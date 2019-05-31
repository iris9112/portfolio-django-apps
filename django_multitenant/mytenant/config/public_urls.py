from django.contrib import admin
from django.urls import path

from tenants.views import TenantsHome

urlpatterns = [
    path('', TenantsHome.as_view(), name='home_public'),
    path('admin/', admin.site.urls),
]
