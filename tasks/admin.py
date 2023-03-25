from django.contrib import admin
from .models import Tasks

# Register your models here.

class taskAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion',)

admin.site.register(Tasks, taskAdmin)
