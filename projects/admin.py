from django.contrib import admin
from .models import Project, VisitorStatistic

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'created_at')
    fields = ('title', 'description', 'github_link', 'demo_link', 'project_image', 'project_type')


@admin.register(VisitorStatistic)
class VisitorStatisticAdmin(admin.ModelAdmin):
    list_display = ('stat_type', 'count', 'date')
    list_filter = ('stat_type', 'date')
