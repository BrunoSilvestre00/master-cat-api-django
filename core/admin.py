from core.tasks import upload_questions_json
from .models import UploadQuestions
from django.contrib import admin


@admin.register(UploadQuestions)
class UploadQuestionsAdmin(admin.ModelAdmin):
    JSON = 'json'
    
    FILE_EXTENSION_MAP = {
        JSON: upload_questions_json,
    }
    
    readonly_fields = ('uuid', 'status', 'result')
    
    def save_model(self, request, obj, form, change):
        name = obj.file.name
        ext = name.split('.')[-1] 
        
        obj.status = UploadQuestions.PROCESSING
        obj.save()
        
        try:
            count = self.FILE_EXTENSION_MAP[ext](obj.file)
            
            obj.status = UploadQuestions.FINISHED
            obj.result = f'{count} questions uploaded.'
        except Exception as e:
            obj.status = UploadQuestions.ERROR
            obj.result = str(e)
        finally:
            obj.save()
