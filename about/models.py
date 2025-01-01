from django.db import models
'''
class Profile(models.Model):
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')  # Ensure this field exists
    about_me = models.TextField()
    profile_photo = models.ImageField(upload_to='uploads/')
    cv = models.FileField(upload_to='uploads/')
    github_link = models.URLField(max_length=200, blank=True, null=True)  # GitHub Profile Link
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)  # LinkedIn Profile Link

    def __str__(self):
        return self.name
'''
class Profile(models.Model):
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    email = models.EmailField(default='example@example.com')  # User's email address (for display)
    recipient_email = models.EmailField(default='admin@example.com')  # Admin email for receiving messages
    about_me = models.TextField()
    profile_photo = models.ImageField(upload_to='uploads/')
    cv = models.FileField(upload_to='uploads/')
    github_link = models.URLField(max_length=200, blank=True, null=True)
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)

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
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=SKILL_TYPES, default='Other')  # Add this field

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




