import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField("UUID", default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        db_table = "user"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

