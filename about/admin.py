from django import forms
from django.contrib import admin
from .models import Profile, Experience, Education, Skill, Project
from .fontawesome_icons import FONT_AWESOME_ICONS


from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from .models import Metrics
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from django.utils.timezone import now, timedelta

class MetricsAdmin(admin.ModelAdmin):
    change_list_template = "admin/about/metrics_dashboard.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.metrics_dashboard_view), name='metrics_dashboard'),
        ]
        return custom_urls + urls

    def metrics_dashboard_view(self, request):
        # Get filtering parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            # Default to the last 7 days
            end_date = now()
            start_date = end_date - timedelta(days=7)

        metrics = Metrics.objects.filter(timestamp__range=[start_date, end_date])

        # Group data by event type
        data = {}
        for event_type, _ in Metrics.EVENT_TYPES:
            filtered_data = metrics.filter(event_type=event_type)
            data[event_type] = filtered_data.values('timestamp', 'count')

        context = {
            'metrics': metrics,
            'start_date': start_date,
            'end_date': end_date,
            'data': data,
        }
        return render(request, 'admin/about/metrics_dashboard.html', context)

    def plot_chart(self, metrics, event_type):
        # Filter data for the event type
        data = metrics.filter(event_type=event_type)

        timestamps = [metric['timestamp'] for metric in data]
        counts = [metric['count'] for metric in data]

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, counts, marker='o', label=event_type.capitalize())

        plt.title(f'{event_type.capitalize()} Analytics')
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.legend()

        # Format x-axis dates
        plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        # Save chart to a BytesIO buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return HttpResponse(buffer, content_type='image/png')


admin.site.register(Metrics, MetricsAdmin)


# Custom SkillAdminForm
class SkillAdminForm(forms.ModelForm):
    icon = forms.ChoiceField(
        choices=FONT_AWESOME_ICONS,  # Use the predefined list of icons
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Skill
        fields = '__all__'


# SkillAdmin
class SkillAdmin(admin.ModelAdmin):
    form = SkillAdminForm  # Attach the custom form
    list_display = ('name', 'type', 'level', 'icon')
    search_fields = ('name',)
    list_filter = ('type',)


admin.site.register(Skill, SkillAdmin)

# ProjectAdmin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

# ProfileAdmin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation', 'email', 'github_link', 'linkedin_link', 'recipient_email')
    list_editable = ('github_link', 'linkedin_link', 'recipient_email')

# ExperienceAdmin
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'start_date', 'end_date')

# EducationAdmin
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'year')
