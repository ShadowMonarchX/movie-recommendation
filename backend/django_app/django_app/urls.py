from django.contrib import admin
from django.urls import path , include

urlpatterns = [
     path('api/', include('drf_api.urls.auth_urls')), 
    path("admin/", admin.site.urls),
   
]
