from django.contrib import admin
from .models import *


class AlternativeInline(admin.TabularInline):
    model = Alternative
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'id', '__str__')
    readonly_fields = ('id', 'uuid')
    actions = ['create_pool']
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
    
    def create_pool(self, request, queryset):
        QuestionPool.create_pool(queryset)
    
    create_pool.short_description = "Criar Banco de Questões"


class QuestionInline(admin.TabularInline):
    model = QuestionPoolHasQuestion
    extra = 1


@admin.register(QuestionPool)
class QuestionPoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'uuid', 'get_count')
    readonly_fields = ('id', 'uuid', 'get_count')
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('id', 'uuid', 'name')
        }),
    )
    
    def get_count(self, obj):
        return len(obj)
    
    get_count.short_description = "# Questões"


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'uuid', 'pool')
    readonly_fields = ('id', 'uuid')
    fieldsets = (
        (None, {
            'fields': ('id', 'uuid', 'name', 'pool')
        }),
    )
