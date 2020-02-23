from django.contrib import admin
from index.models import *
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    search_fields = ['full_name','email','message']
    list_display = ('full_name','email')
    readonly_fields = ('date',)
    def has_delete_permission(self, request, obj=None):
        return False


class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ['full_name','email','message']
    list_display = ('full_name','email')
    readonly_fields = ('date',)
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Contact,ContactAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Registered_Players)
admin.site.register(Free)
admin.site.register(Invite_Friend)
admin.site.register(Friends)
