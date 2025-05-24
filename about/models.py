from django.db import models
from django.utils.timezone import now

from django.db import models
from django.utils.timezone import now

class Metrics(models.Model):
    EVENT_TYPES = [
        ('linkedin', 'LinkedIn Click'),
        ('github', 'GitHub Click'),
        ('cv', 'CV Download'),
        ('message', 'Message Sent'),
        ('website_view', 'Website View'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    count = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(default=now)
    def get_current_month():
        return now().month

    def get_current_year():
        return now().year

    month = models.PositiveSmallIntegerField(default=get_current_month, editable=False)
    year = models.PositiveSmallIntegerField(default=get_current_year, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.month = self.timestamp.month
            self.year = self.timestamp.year
        super().save(*args, **kwargs)

    @classmethod
    def increment_website_view(cls):
        now_time = now()
        obj, created = cls.objects.get_or_create(
            event_type='website_view',
            month=now_time.month,
            year=now_time.year,
            defaults={'timestamp': now_time}
        )
        if not created:
            obj.count += 1
            obj.timestamp = now_time
            obj.save(update_fields=['count', 'timestamp'])
        return obj

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')} (Count: {self.count})"


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




