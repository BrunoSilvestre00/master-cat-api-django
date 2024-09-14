import uuid
import arrow
from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import SoftDeletableModel, TimeStampedModel


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


class UserToken(TimeStampedModel):
    TOKEN_LIFETIME = 60 * 60 * 24 * 7  # 7 days

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    class Meta:
        db_table = "user_token"
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        
    def save(self, *args, **kwargs):
        self.token = uuid.uuid4()
        super().save(*args, **kwargs)

    def is_valid(self):
        return (
            arrow.get(self.modified).shift(seconds=self.TOKEN_LIFETIME) > arrow.utcnow()
        )
