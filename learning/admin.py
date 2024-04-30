from django.contrib import admin
from .models import *


class AlternativeInline(admin.TabularInline):
    model = Alternative
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', '__str__')
    readonly_fields = ('id', 'uuid')
    inlines = [AlternativeInline]
    fieldsets = (
        (None, {
            'fields': ('id', 'uuid')
        }),
        ('Parâmetros IRT', {
            'fields': ('discrimination', 'difficulty', 'guess')
        }),
        ('Parâmetros CDM', {
            'fields': ()
        }),
        ('Conteúdo', {
            'fields': ('statement',)
        }),
    )