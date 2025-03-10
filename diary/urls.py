from django.urls import path
from .views import (
    note_interface,
    note_detail,
    note_detail_ajax,
    note_insights,
)

urlpatterns = [
    path('', note_interface, name='note_interface'),
    path('notes/<int:pk>/', note_detail, name='note_detail'),
    path('notes/<int:pk>/json/', note_detail_ajax, name='note_detail_ajax'),
    path('insights/', note_insights, name='note_insights'),
]
