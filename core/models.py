from django.db import models
from core.utilities.database_utilties import get_next_id
from django.utils import timezone


class BaseModel(models.Model):
    auto_last_updated = True

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk in (None, '', 'new'):
            table_name = self._meta.db_table
            length = self._meta.pk.max_length
            new_id = get_next_id(table_name, length)

            # setattr(self, self._meta.pk.attname, new_id)
            self.pk = new_id

        user_id = kwargs.pop('user_id', None)
        if user_id and hasattr(self, 'last_updated_by_user_id'):
            self.last_updated_by_user_id = user_id

        # if self.auto_last_updated:
        #     setattr(self, 'last_updated', timezone.now())

        super(BaseModel, self).save(*args, **kwargs)
