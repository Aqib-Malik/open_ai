from django.db import models
from Api.models.softdelete import SoftDeleteMixin
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class Appointment(SoftDeleteMixin):
    PENDING = 0
    APPROVED = 1
    COMPLETED = 2
    CANCEL = 3
    MISSED = 4

    STATUS_CHOICES = (
        (PENDING, 0),
        (APPROVED, 1),
        (COMPLETED, 2),
        (CANCEL, 3),
        (MISSED, 4),
    )
    status              = models.IntegerField(default=0, choices=STATUS_CHOICES)
    fees                = models.FloatField()
    is_paid             = models.BooleanField(default=False)
    paid_at             = models.DateTimeField(blank=True, null=True)
    patient             = models.CharField(max_length=50)
    doctor              = models.CharField(max_length=50)
    scheduled_date      = models.DateTimeField()
    department          = models.CharField(max_length=50)
    spec_share          = models.FloatField(default=0)
    govt_share          = models.FloatField(default=0)
    hosp_amenity_share  = models.FloatField(default=0)
    staff_share         = models.FloatField(default=0)
    total_fees          = models.IntegerField(default=0)
    # approved_by         = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    # created_by          = models.ForeignKey('User', related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    updated_at          = models.DateTimeField(auto_now=True)
    # updated_by          = models.ForeignKey('User', related_name='+', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.patient)

    # def save(self,*args,**kwargs):
    #     if not self.pk:
    #         self.department = self.doctor.department
    #         return super().save(*args,**kwargs)
    #     else:
    #         return super().save(*args,**kwargs)

    # @property
    # def consumer_number(self):
    #     return str(self.department.hospital.consumer_number_opd)+settings.APPOINTMENT_CN+str(self.id)