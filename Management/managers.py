from django.db import models

class TypeManager(models.Manager):

    use_for_related_fields = True

    def type(self, type):
        return self.filter(type=type)
