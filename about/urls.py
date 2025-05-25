# about/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_view, name='about'),
    path('send-contact-email/', views.send_contact_email, name='send_contact_email'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]