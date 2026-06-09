from django.contrib import admin
from .models import SchoolSettings, User, Lesson, Package
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'email']
    list_filter = ['role']

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['student', 'hours_total', 'hours_used']
    list_filter = ['student']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['student', 'instructor', 'date', 'location']
    list_filter = ['instructor']

admin.site.register(SchoolSettings)