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
