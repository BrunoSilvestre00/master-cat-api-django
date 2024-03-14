from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.forms.models import model_to_dict

from core.fields import AutoCreatedField, AutoLastModifiedField
from core.managers import SoftDeletableManager, SoftDeletableUserManager


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    ...
    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True


class ChangedModel(models.Model):

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ChangedModel, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def cache_key(self):
        key = self.uuid if self.uuid else self.pk
        return "{0}:{1}".format(type(self).__name__.lower(), key)

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = []

        for k, v in d1.items():
            v1 = v
            v2 = d2[k]
            if v1 != v2:
                if isinstance(v, ImageFieldFile):
                    v1 = str(v1)
                    v2 = str(v2)
                diffs.append((k, (v1, v2)))

        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                                           self._meta.fields])
    
    @property
    def get_admin_url(self):
        from django.urls import reverse
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class SoftDeletableModel(ChangedModel, TimeStampedModel):
    """
    An abstract base class model with a ``removed`` field that
    marks entries that are not going to be used anymore, but are
    kept in db for any reason.
    Default manager returns only not-removed entries.
    """
    removed = models.DateTimeField(null=True, default=None, editable=False)

    objects = SoftDeletableManager()    
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(SoftDeletableModel, self).save(*args, **kwargs)
        self.__initial = self._dict

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``removed`` field to now).
        Actually delete object if setting ``soft`` to None.
        """
        if soft:
            self.removed = now()
            self.save(using=using)
        else:
            return super(SoftDeletableModel, self).delete(using=using, *args, **kwargs)


class SoftDeletableUserModel(SoftDeletableModel):

    objects = SoftDeletableUserManager()

    class Meta:
        abstract = True
