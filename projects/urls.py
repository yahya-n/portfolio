from django.urls import path
from .views import project_list_view, log_statistic

urlpatterns = [
    path('', project_list_view, name='projects'),
    path('log-stat/<str:stat_type>/', log_statistic, name='log_stat'),
]
