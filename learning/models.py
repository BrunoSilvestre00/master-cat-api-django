import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from core.models import SoftDeletableModel


class IRTParams(models.Model):
    """
    Fields used to store the parameters for the IRT model.
    ...
    """
    discrimination = models.FloatField("Discriminação", default=1.0)
    difficulty = models.FloatField("Dificuldade", default=0.0)
    guess = models.FloatField("Chute", default=0.0)
    
    class Meta:
        abstract = True


class CDMParams(models.Model):
    """
    Fields used to store the parameters for the CDM model: DINA and DINO
    ...
    """
    slip = models.FloatField("Deslize", default=0.0)
    guess = models.FloatField("Chute", default=0.0)
    
    class Meta:
        abstract = True

class QuestionMetadata(IRTParams, CDMParams):
    """
    Merge Class to store CAT metadata about a question.
    ...
    """
    
    class Meta:
        abstract = True


class Question(SoftDeletableModel, QuestionMetadata):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    statement = CKEditor5Field("Enunciado")

    class Meta:
        db_table = "questions"
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self) -> str:
        return f'{self.pk} - {self.statement[:10]}...'
    

class Alternative(SoftDeletableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    text = CKEditor5Field("Texto")
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


class Assessment(SoftDeletableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField("Nome", max_length=255)
    pool = models.ForeignKey(QuestionPool, on_delete=models.CASCADE, related_name="assessments")
    
    class Meta:
        db_table = "assessments"
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'

