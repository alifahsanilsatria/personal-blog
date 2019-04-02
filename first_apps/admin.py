from django.contrib import admin
from first_apps.models import Post,Comment,Draft	
from mediumeditor.admin import MediumEditorAdmin

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Draft)

class DraftAdmin(MediumEditorAdmin, admin.ModelAdmin):
    mediumeditor_fields = ('text',)