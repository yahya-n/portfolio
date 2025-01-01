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

def send_contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Construct the email
        subject = f"Message from {name} via Portfolio Contact Form"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        recipient_list = ['abdulkuddoosyahya@gmail.com']  # Replace with your personal email

        try:
            send_mail(subject, body, email, recipient_list)
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

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
