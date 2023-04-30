from django.db import models

class SoftDeleteMixin(models.Model):
    deleted         = models.BooleanField(default=False)

    class Meta:
        abstract = True
    
    def delete(self):
        self.deleted = True
        self.save()
        
    def permdelete(self):
        return super().delete()