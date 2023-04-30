from Api.models.softdelete import SoftDeleteMixin
from django.db import models
import uuid

def get_hospital_image_path(self, filename):
    return f'hospital_images/hospitals/{self.pk}/{str(uuid.uuid4())}.png'

def get_default_hospital_image_path():
    return f'hospital_images/{"default_hospital.png"}'

class Hospital(SoftDeleteMixin):
    CATEGORY1A = 0
    CATEGORY1B = 1
    CATEGORY2 = 2
    CATEGORY3 = 3

    HOSPITAL_TYPE_CHOICES = (
        (CATEGORY1A, 'CATEGORY1A'),
        (CATEGORY1B, 'CATEGORY1B'),
        (CATEGORY2, 'CATEGORY2'),
        (CATEGORY3, 'CATEGORY3'),
    )
    name                        = models.CharField(max_length=100)
    image                       = models.ImageField(max_length=255, upload_to=get_hospital_image_path, null=True, blank=True, default=get_default_hospital_image_path)
    hospital_type               = models.IntegerField(default=0, choices=HOSPITAL_TYPE_CHOICES)
    stoppage_charges            = models.IntegerField(default=0)
    consumer_number_opd         = models.CharField(max_length=10,default=12345)
    consumer_number_ipd         = models.CharField(max_length=10, default=12345)
    consumer_number_opd_refund  = models.CharField(max_length=10, default=12345)
    consumer_number_ipd_refund  = models.CharField(max_length=10, default=12345)
    created_at                  = models.DateTimeField(auto_now_add=True)
    created_by                  = models.ForeignKey('User', related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    updated_at                  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    