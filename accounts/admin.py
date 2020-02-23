from .models import *
from django.contrib import admin



class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user','phone_no','registration_no']
    list_filter = ['registration_no','user','passing_year']
    list_display = ('user','registration_no','passing_year')
    readonly_fields = ('user','phone_no','registration_no','passing_year')
    list_per_page = 20


admin.site.register(UserProfile,UserProfileAdmin)
