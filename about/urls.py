from django.urls import path
from .views import about_view,send_contact_email

urlpatterns = [
    path('', about_view, name='about'),
    path('send-email/', send_contact_email, name='send_contact_email'),
]
