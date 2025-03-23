from django.shortcuts import render
from .models import Profile, Experience, Education, Skill, Project
'''
def about_view(request):
    profile = Profile.objects.first()
    experience = Experience.objects.all()
    education = Education.objects.all()
    skills = Skill.objects.all()
    frontend_skills = skills.filter(type='FE')
    backend_skills = skills.filter(type='BE')
    projects = Project.objects.all()
    return render(request, 'index.html', {
        'profile': profile,
        'experience': experience,
        'education': education,
        'frontend_skills': frontend_skills,
        'backend_skills': backend_skills,
        'projects': projects,
    })

def about_view(request):
    profile = Profile.objects.first()
    experience = Experience.objects.all()
    education = Education.objects.all()
    skills = Skill.objects.all()
    frontend_skills = skills.filter(type='Frontend')
    backend_skills = skills.filter(type='Backend')
    other_skills = skills.filter(type='Other')
    projects = Project.objects.all()
    return render(request, 'index.html', {
        'profile': profile,
        'experience': experience,
        'education': education,
        'frontend_skills': frontend_skills,
        'backend_skills': backend_skills,
        'other_skills': other_skills,
        'projects': projects,
    })'''
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from .models import Profile

from django.http import JsonResponse
from .models import Metrics
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth

from django.http import HttpResponse
from .models import Metrics
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from django.utils.timezone import now, timedelta
from io import BytesIO

def metrics_chart_view(request, event_type):
    # Filter data for the past 7 days
    end_date = now()
    start_date = end_date - timedelta(days=7)
    metrics = Metrics.objects.filter(event_type=event_type, timestamp__range=[start_date, end_date])

    # Prepare data
    timestamps = [metric.timestamp for metric in metrics]
    counts = [metric.count for metric in metrics]

    # Generate the chart
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


def track_event(request, event_type):
    if request.method == "POST":
        if event_type in dict(Metrics.EVENT_TYPES).keys():
            # Track the interaction
            Metrics.objects.create(event_type=event_type, count=1)
            return JsonResponse({'success': True, 'message': f'{event_type} interaction recorded.'})
    return JsonResponse({'success': False, 'message': 'Invalid event type or request method.'})

def send_contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Retrieve the recipient email from the Profile model
        profile = Profile.objects.first()  # Assumes only one profile exists
        recipient_email = profile.recipient_email if profile else 'default@example.com'

        # Construct the email
        subject = f"Message from {name} via Portfolio Contact Form"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = 'poartalzz@gmail.com'  # Use EMAIL_HOST_USER to avoid Gmail rejection

        try:
            send_mail(subject, body, from_email, [recipient_email])
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Error: {str(e)}"})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

def about_view(request):
    profile = Profile.objects.first()
    experience = Experience.objects.all()
    education = Education.objects.all()
    skills = Skill.objects.all()  # Fetch all skills
    frontend_skills = skills.filter(type='Frontend')
    backend_skills = skills.filter(type='Backend')
    other_skills = skills.filter(type='Other')
    projects = Project.objects.all()

    return render(request, 'index.html', {
        'profile': profile,
        'experience': experience,
        'education': education,
        'frontend_skills': frontend_skills,
        'backend_skills': backend_skills,
        'other_skills': other_skills,
        'projects': projects,
    })
