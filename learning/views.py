from rest_framework import viewsets, status
from rest_framework.response import Response
from plumber.client import PlumberClient
from .models import *
from .serializers import *
from .services import QuestionPoolService, UserAssessmentService


class UserAssessmentViewset(viewsets.ModelViewSet):
    serializer_class = None

    def get_queryset(self):
        return UserAssessmentViewset.objects\
            .filter(user_id=self.request.user.id)

    def create(self, request):
        # TODO: improve security and error handling
        
        assessment = Assessment.objects.get(
            uuid=request.data.get('assessment')
        )
        questions = assessment.pool.questions.all().order_by('questionpoolhasquestion__order')
        
        questions_data = QuestionPlumberSerializer(
            questions, many=True
        ).data
        
        plumb_response = PlumberClient().start_assesment(questions_data)
        
        # TODO: dinamically set user_id
        user_assessment, _ = UserAssessment.objects.update_or_create(
            user_id=2,
            assessment_id=assessment.id,
            defaults=dict(
                next_index=plumb_response.get('next_index', 0),
                design=plumb_response.get('design', None),
            )
        )
        
        next_question = QuestionPoolService.get_next_question(
            assessment.pool_id, plumb_response.get('next_index')
        )
        assesssment_data: dict = AssessmentSerializer(assessment).data
        
        data = {
            'user_assessment': user_assessment.uuid,
            'status': UserAssessment.IN_PROGRESS,
            'next_question': QuestionSerializer(next_question).data,
            **assesssment_data
        }
        
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        # TODO: improve security and error handling
        
        user_assessment = UserAssessment.objects\
            .select_related('assessment').get(uuid=pk)
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
            
            UserAssessmentService.get_design_data(user_assessment)
            
            payload = { 
                'user_assessment': user_assessment.uuid,
                'status': UserAssessment.COMPLETED,
                'next_question': None,
                **assessment_data
            }
            
            return Response(payload, status=status.HTTP_200_OK)
        
        user_assessment.save(update_fields=['next_index', 'design'])
            
        next_question = QuestionPoolHasQuestion.objects\
            .select_related('question').get(
                pool_id=user_assessment.assessment.pool_id,
                order=plumb_response.get('next_index')
            ).question
        
        data = {
            'user_assessment': user_assessment.uuid,
            'status': UserAssessment.IN_PROGRESS,
            'next_question': QuestionSerializer(next_question).data,
            **assessment_data
        }
        
        return Response(data, status=status.HTTP_200_OK)
