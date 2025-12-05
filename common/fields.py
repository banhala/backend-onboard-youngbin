from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper


class ForceAutoNowDateTimeField(models.DateTimeField):

    def db_type(self, connection: BaseDatabaseWrapper) -> str:
        if connection.vendor == "mysql" and self.auto_now:
            result = "datetime(6) ON UPDATE CURRENT_TIMESTAMP(6)"
        else:
            result = super().db_type(connection)
        return result
