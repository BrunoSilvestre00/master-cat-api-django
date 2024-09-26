from learning.models import UserAssessment, MirtDesignData, QuestionPoolHasQuestion, Question
from plumber.client import PlumberClient

class QuestionPoolService(object):
    
    @classmethod
    def get_next_question(cls, pool_id: int, index: int) -> Question:
        return QuestionPoolHasQuestion.objects.get(
            pool_id=pool_id,
            order=index
        ).question


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
