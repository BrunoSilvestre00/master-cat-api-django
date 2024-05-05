import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import SoftDeletableModel


class User(AbstractUser, SoftDeletableModel):
    uuid = models.UUIDField("UUID", default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        db_table = "user"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class StudentUser(User):
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        proxy = True
