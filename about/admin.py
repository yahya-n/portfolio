from django.contrib import admin
from .models import Profile, Experience, Education, Skill

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'start_date', 'end_date')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'year')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'level')
