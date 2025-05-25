from django.db import models
from django.utils.timezone import now

from django.db import models
from django.utils.timezone import now

from django.db import models
from django.utils.timezone import now
from datetime import timedelta

from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncMonth , TruncDay, TruncYear

class Metrics(models.Model):
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('linkedin', 'LinkedIn Click'),
        ('github', 'GitHub Click'),
        ('twitter', 'Twitter Click'),
        ('download_cv', 'CV Download'),
        ('send_message', 'Message Sent'),
    ]
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    timestamp = models.DateTimeField(default=now)
    count = models.IntegerField(default=1)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.CharField(max_length=512, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Metrics"
        ordering = ['-timestamp']

    
    @classmethod
    def get_current_month(cls):
        """Get metrics for current month grouped by day"""
        today = now()
        first_day = today.replace(day=1)
        return cls.objects.filter(
            timestamp__range=[first_day, today]
        ).annotate(
            day=TruncDay('timestamp')
        ).values('day', 'event_type').annotate(
            total=Count('id')
        ).order_by('day')

    @classmethod
    def get_current_year(cls):
        """Get metrics for current year grouped by month"""
        today = now()
        first_day = today.replace(month=1, day=1)
        return cls.objects.filter(
            timestamp__range=[first_day, today]
        ).annotate(
            month=TruncMonth('timestamp')
        ).values('month', 'event_type').annotate(
            total=Count('id')
        ).order_by('month')
    
    @classmethod
    def get_daily_stats(cls, days=30):
        """Get daily stats for the last X days"""
        end_date = now()
        start_date = end_date - timedelta(days=days)
        
        return cls.objects.filter(
            timestamp__range=[start_date, end_date]
        ).annotate(
            day=TruncDay('timestamp')
        ).values('day', 'event_type').annotate(
            count=Count('id')
        ).order_by('day')
    
    @classmethod
    def get_top_events(cls, limit=5):
        """Get most frequent events"""
        return cls.objects.values('event_type').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
    
    @classmethod
    def get_visitor_stats(cls):
        """Get visitor statistics"""
        total_visitors = cls.objects.values('session_key').distinct().count()
        returning_visitors = cls.objects.values('session_key').annotate(
            visit_count=Count('id')
        ).filter(visit_count__gt=1).count()
        
        return {
            'total': total_visitors,
            'returning': returning_visitors,
            'new': total_visitors - returning_visitors
        }

    def __str__(self):
        return f"{self.get_event_type_display()} at {self.timestamp}"

class Profile(models.Model):
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    typewriter = models.CharField(max_length=100, default='')  # Typewriter effect text
    email = models.EmailField(default='example@example.com')  # User's email address (for display)
    recipient_email = models.EmailField(default='admin@example.com')  # Admin email for receiving messages
    about_me = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='uploads/')
    cv = models.FileField(upload_to='uploads/')
    about_quote = models.CharField(max_length=255)
    github_link = models.URLField(max_length=200, blank=True, null=True)
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Experience(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.role} at {self.company}"

class Education(models.Model):
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.degree} from {self.institution}"
'''
class Skill(models.Model):
    SKILL_TYPE_CHOICES = [
        ('FE', 'Frontend'),
        ('BE', 'Backend'),
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(choices=SKILL_TYPE_CHOICES, max_length=2)
    level = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
'''
class Skill(models.Model):
    SKILL_TYPES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Softskills', 'Softskills'),
        ('Tools', 'Tools'),
    ]

    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=SKILL_TYPES, default='Tools')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField()
    demo_link = models.URLField()
    project_image = models.ImageField(upload_to='uploads/projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




