from django.contrib import admin
from .models import AboutMe, RequestContent, ModelsChange


class AdminModelsChanges(admin.ModelAdmin):
    list_display = ('model', 'datetime', 'action')

admin.site.register(AboutMe)
admin.site.register(RequestContent)
admin.site.register(ModelsChange, AdminModelsChanges)
