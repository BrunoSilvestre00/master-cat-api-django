from requests import Response
from rest_framework import viewsets, status
from plumber.client import PlumberClient
from .models import Assessment, UserAssessment, Alternative
from .serializers import *


class UserAssessmentViewset(viewsets.ModelViewSet):
    serializer_class = None

    def get_queryset(self):
        return UserAssessmentViewset.objects\
            .filter(user_id=self.request.user.id)

    def create(self, request, uuid=None):
        # TODO: improve security and error handling
        
        assessment = Assessment.objects.get(
            uuid=request.data.get('assessment')
        )
        questions = assessment.pool.questions.all()
        
        questions_data = QuestionPlumberSerializer(
            questions, many=True
        ).data
        
        plumb_response = PlumberClient().start_assesment(questions_data)
        
        user_assessment, _ = UserAssessment.objects.update_or_create(
            user_id=1,
            assessment_id=assessment.id,
            defaults=dict(
                next_index=plumb_response.get('next_index', 0),
                design=plumb_response.get('design', None),
            )
        )
        
        next_question = questions.select_related('alternatives')\
            .get(uuid=plumb_response.get('next_item'))
        assesssment_data: dict = AssessmentSerializer(assessment).data
        
        data = {
            'user_assessment': user_assessment.uuid,
            'status': UserAssessment.IN_PROGRESS,
            'next_question': QuestionSerializer(next_question).data,
            **assesssment_data
        }
        
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, uuid=None):
        # TODO: improve security and error handling
        
        user_assessment = UserAssessment.objects\
            .select_related('assessment').get(uuid=uuid)
        payload = request.data.copy()
        
        alternative = Alternative.objects.get(uuid=payload.get('alternative'))
        
        plumb_response = PlumberClient().next_item(
            answer=int(alternative.is_correct),
            previous_index=user_assessment.next_index,
            encoded_design=user_assessment.design,
        )
        
        user_assessment.next_index = plumb_response.get('next_index', 0)
        user_assessment.design = plumb_response.get('design', None)
        stop_assessment = plumb_response.get('stop', False)
        assessment_data: dict = AssessmentSerializer(user_assessment.assessment).data
        
        if stop_assessment:
            user_assessment.status = UserAssessment.COMPLETED
            user_assessment.save(update_fields=['next_index', 'design', 'status'])
            payload = { 
                'user_assessment': user_assessment.uuid,
                'status': UserAssessment.COMPLETED,
                'next_question': None,
                **assessment_data
            }
            
            return Response(payload, status=status.HTTP_200_OK)
        
        user_assessment.save(update_fields=['next_index', 'design'])
        
        next_question = user_assessment.assessment.pool.questions\
            .selected_related('alternatives')\
            .get(uuid=plumb_response.get('next_item'))
        
        data = {
            'user_assessment': user_assessment.uuid,
            'status': UserAssessment.IN_PROGRESS,
            'next_question': QuestionPlumberSerializer(next_question).data,
            **assessment_data
        }
        
        return Response(data, status=status.HTTP_200_OK)
