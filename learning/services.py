from learning.models import Assessment, UserAssessment, MirtDesignData, QuestionPoolHasQuestion, Question
from user.models import User, UserPoolHasAssessment, UserPoolHasUser
from plumber.client import PlumberClient

class QuestionPoolService(object):
    
    @classmethod
    def get_next_question(cls, pool_id: int, index: int) -> Question:
        return QuestionPoolHasQuestion.objects.get(
            pool_id=pool_id,
            order=index
        ).question


class AssessmentService(object):
    
    @classmethod
    def get_user_assessments(cls, user: User):
        qs = Assessment.objects.filter(active=True)
        if not user.is_superuser:
            user_pool_ids = UserPoolHasUser.objects.filter(
                user__id=user.id).values_list('pool_id', flat=True)
            user_assessments = UserPoolHasAssessment.objects.filter(
                pool_id__in=user_pool_ids).values_list('assessment_id', flat=True)
            qs = qs.filter(id__in=user_assessments)
        return qs


class UserAssessmentService(object):
    
    @classmethod
    def get_design_data(cls, user_assessment: UserAssessment, clear_design: bool = False) -> MirtDesignData:
        design_data = PlumberClient().get_design_data(user_assessment.design)
        
        if clear_design:
            user_assessment.design = None
            user_assessment.save(update_fields=['design'])
        
        return MirtDesignData.objects.create(
            user_assessment_id=user_assessment.id,
            **design_data
        )
