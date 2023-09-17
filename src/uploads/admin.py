from django.contrib import admin
from . import models

# Register your models here.


class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'uploaded_by', 'uploaded_on']
    readonly_fields = ['uploaded_on', 'uploaded_by']
    ordering = ['-uploaded_on']
    list_filter = ['uploaded_on', 'uploaded_by']
    search_fields = ['name']
    list_display_links = ['name']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.ImageUpload, ImageUploadAdmin)
