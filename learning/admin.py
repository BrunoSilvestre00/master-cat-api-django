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
            'fields': [f.name for f in IRTParams._meta.fields]
        }),
        ('Parâmetros CDM', {
            'fields': [f.name for f in CDMParams._meta.fields]
        }),
        ('Conteúdo', {
            'fields': ('statement',)
        }),
    )