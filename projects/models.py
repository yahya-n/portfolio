from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField()
    demo_link = models.URLField()
    project_image = models.ImageField(upload_to='uploads/projects/', blank=True, null=True)
    project_type = models.CharField(max_length=50)  # Example: Django, Flask, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VisitorStatistic(models.Model):
    STAT_TYPE_CHOICES = [
        ('Download CV', 'Download CV'),
        ('Contact', 'Contact'),
        ('Visit', 'Visit'),
    ]
    stat_type = models.CharField(max_length=50, choices=STAT_TYPE_CHOICES)
    count = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.stat_type} - {self.count} on {self.date}"
