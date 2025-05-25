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
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_datetime

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from .models import Metrics
from django.utils.timezone import now, timedelta
from django.utils.dateparse import parse_datetime
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from .models import Metrics
from django.utils.timezone import now, timedelta
from django.utils.dateparse import parse_datetime

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from .models import Metrics
from django.utils.timezone import now, timedelta
from django.db.models import Count, Q
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from datetime import datetime

class MetricsAdmin(admin.ModelAdmin):
    change_list_template = "admin/about/metrics_dashboard.html"
    list_display = ('event_type', 'timestamp', 'ip_address')
    list_filter = ('event_type', 'timestamp')
    date_hierarchy = 'timestamp'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.metrics_dashboard), name='metrics_dashboard'),
            path('dashboard/data/', self.admin_site.admin_view(self.metrics_data), name='metrics_data'),
        ]
        return custom_urls + urls

    def metrics_dashboard(self, request):
        today = now()
        first_day_of_month = today.replace(day=1)
        
        context = {
            'title': 'Portfolio Analytics Dashboard',
            'default_start': first_day_of_month.strftime('%Y-%m-%d'),
            'default_end': today.strftime('%Y-%m-%d'),
        }
        return render(request, 'admin/about/metrics_dashboard.html', context)

    def metrics_data(self, request):
        # Get parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        group_by = request.GET.get('group_by', 'day')  # day, month, or year
        
        # Set default dates (current month)
        today = now()
        if not start_date or not end_date:
            start_date = today.replace(day=1)
            end_date = today
        else:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
        
        # Determine grouping
        if group_by == 'month':
            trunc_func = TruncMonth('timestamp')
            date_format = '%b %Y'
        elif group_by == 'year':
            trunc_func = TruncYear('timestamp')
            date_format = '%Y'
        else:  # default to day
            trunc_func = TruncDay('timestamp')
            date_format = '%b %d'
        
        # Get data
        metrics = Metrics.objects.filter(
            timestamp__date__gte=start_date.date(),
            timestamp__date__lte=end_date.date()
        ).annotate(
            period=trunc_func
        ).values('period', 'event_type').annotate(
            total=Count('id')
        ).order_by('period')
        
        # Get summary statistics
        summary = self.get_summary_stats(start_date, end_date)
        
        # Format data for Chart.js
        event_types = Metrics.EVENT_TYPES
        all_periods = self.generate_periods(start_date, end_date, group_by)
        labels = [period.strftime(date_format) for period in all_periods]
        
        # Initialize datasets
        datasets = []
        colors = {
            'page_view': 'rgba(54, 162, 235, 1)',
            'linkedin': 'rgba(75, 192, 192, 1)',
            'github': 'rgba(153, 102, 255, 1)',
            'twitter': 'rgba(255, 159, 64, 1)',
            'download_cv': 'rgba(255, 99, 132, 1)',
            'send_message': 'rgba(255, 206, 86, 1)',
        }
        
        for event_type, event_name in event_types:
            data = [0] * len(all_periods)
            
            # Fill in data for this event type
            for m in metrics:
                if m['event_type'] == event_type:
                    period_str = m['period'].strftime(date_format)
                    try:
                        idx = labels.index(period_str)
                        data[idx] = m['total']
                    except ValueError:
                        continue
            
            datasets.append({
                'label': event_name,
                'data': data,
                'borderColor': colors[event_type],
                'backgroundColor': colors[event_type].replace('1)', '0.2)'),
                'borderWidth': 2,
                'tension': 0.1
            })
        
        return JsonResponse({
            'labels': labels,
            'datasets': datasets,
            'summary': summary
        })
    
    def generate_periods(self, start_date, end_date, group_by='day'):
        periods = []
        current = start_date
        
        if group_by == 'month':
            while current <= end_date:
                periods.append(current)
                # Move to first day of next month
                if current.month == 12:
                    current = current.replace(year=current.year+1, month=1, day=1)
                else:
                    current = current.replace(month=current.month+1, day=1)
        elif group_by == 'year':
            while current <= end_date:
                periods.append(current)
                current = current.replace(year=current.year+1, month=1, day=1)
        else:  # day
            while current <= end_date:
                periods.append(current)
                current += timedelta(days=1)
        
        return periods
    
    def get_summary_stats(self, start_date, end_date):
        # Get previous period for comparison
        delta = end_date - start_date
        prev_start = start_date - delta
        prev_end = start_date - timedelta(days=1)
        
        # Current period stats
        current_stats = Metrics.objects.filter(
            timestamp__date__gte=start_date.date(),
            timestamp__date__lte=end_date.date()
        ).aggregate(
            total_page_views=Count('id', filter=Q(event_type='page_view')),
            total_interactions=Count('id', filter=~Q(event_type='page_view')),
            unique_visitors=Count('session_key', distinct=True),
            cv_downloads=Count('id', filter=Q(event_type='download_cv')),
        )
        
        # Previous period stats
        prev_stats = Metrics.objects.filter(
            timestamp__date__gte=prev_start.date(),
            timestamp__date__lte=prev_end.date()
        ).aggregate(
            total_page_views=Count('id', filter=Q(event_type='page_view')),
            total_interactions=Count('id', filter=~Q(event_type='page_view')),
            unique_visitors=Count('session_key', distinct=True),
            cv_downloads=Count('id', filter=Q(event_type='download_cv')),
        )
        
        # Calculate changes
        def calculate_change(current, previous):
            if previous == 0:
                return 'N/A'
            change = ((current - previous) / previous) * 100
            return f"{'+' if change >= 0 else ''}{change:.1f}%"
        
        return {
            'total_page_views': current_stats['total_page_views'] or 0,
            'total_interactions': current_stats['total_interactions'] or 0,
            'unique_visitors': current_stats['unique_visitors'] or 0,
            'cv_downloads': current_stats['cv_downloads'] or 0,
            'page_views_change': calculate_change(
                current_stats['total_page_views'] or 0,
                prev_stats['total_page_views'] or 0
            ),
            'interactions_change': calculate_change(
                current_stats['total_interactions'] or 0,
                prev_stats['total_interactions'] or 0
            ),
            'visitors_change': calculate_change(
                current_stats['unique_visitors'] or 0,
                prev_stats['unique_visitors'] or 0
            ),
            'downloads_change': calculate_change(
                current_stats['cv_downloads'] or 0,
                prev_stats['cv_downloads'] or 0
            ),
        }

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
