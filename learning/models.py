import uuid
from django.db import models

from core.models import SoftDeletableModel


class CATModelsEnum(object):
    # IRT
    RASCH = "rasch"
    TWO_PL = "2pl"
    THREE_PL = "3pl"
    FOUR_PL = "4pl"
    
    # CDM
    DINA = "dina"
    DINO = "dino"
    
    def __iter__(self):
        return iter(self.get_models())
    
    def get_irt_models(self):
        return [self.RASCH, self.TWO_PL, self.THREE_PL, self.FOUR_PL]
    
    def get_cdm_models(self):
        return [self.DINA, self.DINO]
    
    def get_models(self):
        return self.get_irt_models() + self.get_cdm_models()
    
    def get_model_choices(self):
        return [(model, model.upper()) for model in self.get_models()]
    
    
class QuestionMetadata(models.Model):
    """
    Fields used to store CAT metadata about a question.
    ...
    """
    
    class Meta:
        abstract = True


class Question(SoftDeletableModel, QuestionMetadata):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    statement = models.TextField("Enunciado")

    class Meta:
        db_table = "questions"
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self) -> str:
        return f'{self.pk} - {self.statement[:10]}...'
    

class Alternative(SoftDeletableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    text = models.TextField("Texto")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="alternatives")
    is_correct = models.BooleanField("Correta", default=False)
    
    class Meta:
        db_table = "alternatives"
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"

    def __str__(self) -> str:
        return f'{self.pk} - {self.text[:10]}...'



class QuestionPool(SoftDeletableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField("Nome", max_length=255)
    questions = models.ManyToManyField(Question, related_name="pools")
    
    class Meta:
        db_table = "question_pools"
        verbose_name = "Banco de Questões"
        verbose_name_plural = "Bancos de Questões"

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'


class AssessmentMetadata(models.Model):
    """
    Fields used to store CAT metadata about an assessment.
    ...
    """
    
    class Meta:
        abstract = True


class Assessment(SoftDeletableModel, AssessmentMetadata):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField("Nome", max_length=255)
    pool = models.ForeignKey(QuestionPool, on_delete=models.CASCADE, related_name="assessments")
    
    class Meta:
        db_table = "assessments"
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'

