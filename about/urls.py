from django.urls import path
from .views import about_view, send_contact_email, track_event, metrics_chart_view

urlpatterns = [
    path('', about_view, name='about'),
    path('send-email/', send_contact_email, name='send_contact_email'),
    path('track-event/<str:event_type>/', track_event, name='track_event'),
    path('metrics-chart/<str:event_type>/', metrics_chart_view, name='metrics_chart'),
]
