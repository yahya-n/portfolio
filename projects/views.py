from django.shortcuts import render
from .models import Project, VisitorStatistic
from django.http import JsonResponse

from django.shortcuts import render
from .models import Project

def project_list_view(request):
    projects = Project.objects.all()
    print("Debugging Projects:", projects)  # Add this debugging line
    return render(request, 'index.html', {'projects': projects})



def log_statistic(request, stat_type):
    """Logs a visitor statistic."""
    if stat_type not in ['Download CV', 'Contact', 'Visit']:
        return JsonResponse({'error': 'Invalid stat type'}, status=400)
    
    VisitorStatistic.objects.create(stat_type=stat_type, count=1)
    return JsonResponse({'message': f'{stat_type} logged successfully'})
