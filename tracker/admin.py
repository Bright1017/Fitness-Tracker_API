from django.contrib import admin
from .models import CustomUser, Activity

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_filter = ['email']
    search_fields = ['username']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type','duration','distance', 'distance_unit', 'calories', 'date']
    list_filter = ['user', 'activity_type','duration','distance', 'distance_unit', 'calories', 'date']
    search_fields = ['user', 'activity_type','duration','distance', 'distance_unit', 'calories', 'date']