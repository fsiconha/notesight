from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Optionally include your app's URLs:
    path('', include('diary.urls')),  # Make sure diary/urls.py exists if you include it.
]
