from django.db import models

# What does this do????
class TypeManager(models.Manager):

    use_for_related_fields = True

    def type(self, type):
        return self.filter(type=type)
