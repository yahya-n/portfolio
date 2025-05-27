# about/views.py - COMPLETE REPLACEMENT
from django.shortcuts import render
from .models import Profile, Experience, Education, Skill, Project, Metrics
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def track_event(request):
    """Track user interaction events - THIS IS THE KEY FUNCTION"""
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            event_type = data.get('event_type')
            
            print(f"Tracking event: {event_type}")  # Debug line
            
            # Ensure session exists
            if not request.session.session_key:
                request.session.create()
            
            # Create metrics record
            metric = Metrics.objects.create(
                event_type=event_type,
                session_key=request.session.session_key,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                path=request.META.get('HTTP_REFERER', ''),
                timestamp=now()
            )
            
            print(f"Metric created: {metric}")  # Debug line
            
            return JsonResponse({'status': 'success', 'message': f'Tracked {event_type}'})
            
        except Exception as e:
            print(f"Error tracking event: {e}")  # Debug line
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'})

def send_contact_email(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Track contact form submission manually here too
        try:
            if not request.session.session_key:
                request.session.create()
            
            Metrics.objects.create(
                event_type='contact_form_submission',
                session_key=request.session.session_key,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                timestamp=now()
            )
            print("Contact form submission tracked")  # Debug line
        except Exception as e:
            print(f"Error tracking contact form: {e}")

        # Send email
        profile = Profile.objects.first()
        recipient_email = profile.recipient_email if profile else 'default@example.com'

        subject = f"Message from {name} via Portfolio Contact Form"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = 'poartalzz@gmail.com'

        try:
            send_mail(subject, body, from_email, [recipient_email])
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Error: {str(e)}"})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

def about_view(request):
    """Main portfolio view"""
    # Page views are tracked by middleware, so we don't need to track here
    
    profile = Profile.objects.first()
    experience = Experience.objects.all()
    education = Education.objects.all()
    skills = Skill.objects.all()
    frontend_skills = skills.filter(type='Frontend')
    backend_skills = skills.filter(type='Backend')
    database_skills = skills.filter(type='Database')
    tools_skills = skills.filter(type='Tools')
    soft_skills = skills.filter(type='Softskills')
    about_quote = profile.about_quote if profile else None
    location = profile.location if profile else None
    typewriter = profile.typewriter if profile else None
    projects = Project.objects.all()
    title_name = profile.title_name if profile else 'My Portfolio'

    return render(request, 'index.html', {
        'profile': profile,
        'experience': experience,
        'education': education,
        'frontend_skills': frontend_skills,
        'backend_skills': backend_skills,
        'database_skills': database_skills,
        'tools_skills': tools_skills,
        'soft_skills': soft_skills,
        'about_quote': about_quote,
        'location': location,
        'typewriter': typewriter,
        'projects': projects,
        'title_name': title_name,
    })

@login_required
def dashboard_view(request):
    """Admin dashboard view"""
    stats = {
        'page_views': Metrics.objects.filter(event_type='page_view').count(),
        'linkedin_clicks': Metrics.objects.filter(event_type='linkedin').count(),
        'github_clicks': Metrics.objects.filter(event_type='github').count(),
        'twitter_clicks': Metrics.objects.filter(event_type='twitter').count(),
        'cv_downloads': Metrics.objects.filter(event_type='download_cv').count(),
        'contact_submissions': Metrics.objects.filter(event_type='contact_form_submission').count(),
        'unique_visitors': Metrics.objects.values('session_key').distinct().count(),
        'recent_activity': Metrics.objects.order_by('-timestamp')[:10],
    }
    
    # Debug: Print current metrics count
    total_metrics = Metrics.objects.count()
    print(f"Total metrics in database: {total_metrics}")
    for event_type, _ in Metrics.EVENT_TYPES:
        count = Metrics.objects.filter(event_type=event_type).count()
        print(f"{event_type}: {count}")
    
    return render(request, 'metrics_dashboard.html', {'stats': stats})