# diary/urls.py

from django.urls import path
from .views import note_interface, note_detail_ajax, note_detail

urlpatterns = [
    path('', note_interface, name='note_interface'),
    # Existing detail view (if used):
    path('notes/<int:pk>/', note_detail, name='note_detail'),
    # New AJAX endpoint for modal pop-up:
    path('notes/<int:pk>/json/', note_detail_ajax, name='note_detail_ajax'),
]
