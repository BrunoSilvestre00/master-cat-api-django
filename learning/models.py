import uuid
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from core.models import SoftDeletableModel
from user.models import StudentUser


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
    # slipping = models.FloatField("Deslize", default=0.0)
    # guessing = models.FloatField("Chute", default=0.0)
    
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
    questions = models.ManyToManyField(Question, related_name="pools", through="QuestionPoolHasQuestion")
    
    class Meta:
        db_table = "question_pools"
        verbose_name = "Banco de Questões"
        verbose_name_plural = "Bancos de Questões"

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'
    
    def __len__(self) -> int:
        return self.questions.count()
    
    @classmethod
    def create_pool(cls, queryset: list) -> 'QuestionPool':
        pool = cls.objects.create(name="_")
        
        qphq = [
            QuestionPoolHasQuestion(
                pool=pool, question=q, order=i+1
            ) for i, q in enumerate(queryset)
        ]
        QuestionPoolHasQuestion.objects.bulk_create(qphq)
        
        pool.name = f"Pool_{pool.id}_{pool.created}"
        pool.save()
        
        return pool


class QuestionPoolHasQuestion(SoftDeletableModel):
    pool = models.ForeignKey(QuestionPool, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Ordem", default=1)
    
    class Meta:
        db_table = "question_pool_has_questions"
        verbose_name = "Questão no Banco de Questões"
        verbose_name_plural = "Questões nos Bancos de Questões"


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


class UserAssessment(SoftDeletableModel):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    
    STATUS_CHOICES = (
        (IN_PROGRESS, "Em Progresso"),
        (COMPLETED, "Finalizado"),
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name="assessments")
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="users")
    status = models.CharField("Status", max_length=255, choices=STATUS_CHOICES, default=IN_PROGRESS)
    next_index = models.IntegerField("Próximo Índice", default=0)
    design = models.TextField("Design", default=None, null=True, blank=True)
    
    class Meta:
        db_table = "user_has_assessments"
        verbose_name = "Avaliação do Usuário"
        verbose_name_plural = "Avaliações dos Usuários"
