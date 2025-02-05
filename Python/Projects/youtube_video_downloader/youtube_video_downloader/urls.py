from django.contrib import admin
from django.urls import path
from core.views import download_video, custom_404_view, custom_500_view

# Custom error handlers (ensure they are view functions, not strings)
handler404 = custom_404_view
handler500 = custom_500_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", download_video, name="download_video"),
]
