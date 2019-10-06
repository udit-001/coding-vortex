from django.contrib import admin
from .models import Contact

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ['submitted_on']
    list_display = ['id', 'name', 'email', 'message', 'submitted_on']
    list_filter = ['submitted_on']
    list_display_links = ['id', 'name']
    ordering = ['-submitted_on']


admin.site.register(Contact, ContactAdmin)
