from django.db import models
from Api.models.softdelete import SoftDeleteMixin
from django.utils import timezone
from Api.models.user import get_default_profile_image_path, get_profile_image_path

gender_choices = [('male', 'male'), ('female', 'female'), ('others', 'others')]

class Patient(SoftDeleteMixin):
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'

    BLOOD_GROUP_CHOICES = (
        (A_POSITIVE, "A+"),
        (A_NEGATIVE, "A-"),
        (B_POSITIVE, "B+"),
        (B_NEGATIVE, "A-"),
        (O_POSITIVE, "O-"),
        (O_NEGATIVE, "O-"),
        (AB_POSITIVE, "AB+"),
        (AB_NEGATIVE, "AB-")
    )


    SELF = 'Self'
    FATHER = 'Father'
    MOTHER = 'Mother'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    GRAND_FATHER = 'Grand Father'
    GRAND_MOTHER = 'Grand Mother'
    NEPHEW = 'Nephew'
    NIECE = 'Niece'
    COUSIN = 'Cousin'
    UNCLE = 'Uncle'
    AUNT = 'Aunt'
    SON = 'Son'
    DAUGHTER = 'Daughter'
    BROTHER = 'Brother'
    SISTER = 'Sister'
    OTHER = 'Other'

    RELATION_CHOICES = (
        (SELF, 'Self'),
        (FATHER, 'Father'),
        (MOTHER, 'Mother'),
        (HUSBAND, 'Husband'),
        (WIFE, 'Wife'),
        (GRAND_FATHER, 'Grand Father'),
        (GRAND_MOTHER, 'Grand Mother'),
        (NEPHEW, 'Nephew'),
        (NIECE, 'Niece'),
        (COUSIN, 'Cousin'),
        (UNCLE, 'Uncle'),
        (AUNT, 'Aunt'),
        (SON, 'Son'),
        (DAUGHTER, 'Daughter'),
        (BROTHER, 'Brother'),
        (SISTER, 'Sister'),
        (OTHER, 'Other'),
    )

    patient_name             = models.CharField(max_length=100)
    blood_group              = models.CharField(max_length=3, blank=True, null=True, choices=BLOOD_GROUP_CHOICES)
    patient_dob              = models.DateField(blank=True, null=True)
    relation                 = models.CharField(max_length=12, blank=True, null=True, choices=RELATION_CHOICES)
    mr_number                = models.CharField(max_length=50, blank=True, null=True)
    gender                   = models.CharField(max_length=10, choices=gender_choices, default=gender_choices[0][0])
    profile_image            = models.ImageField(max_length=255, upload_to=get_profile_image_path, null=True, blank=True, default=get_default_profile_image_path)
    cards_printed            = models.IntegerField(default=0)
    user                     = models.ForeignKey('User', on_delete=models.CASCADE)
    created_by               = models.ForeignKey('User', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    created_at               = models.DateTimeField(auto_now_add=True)
    updated_at               = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient_name
    
    class Meta:
        unique_together = ('user', 'patient_name', 'relation', 'deleted')

    def save(self,*args,**kwargs):
        if self.pk:
            if self.mr_number is None or len(str(self.mr_number))==0:
                self.mr_number=str(timezone.now().year) + str(timezone.now().month) + str(self.id)
            return super().save(*args,**kwargs)
        else:
            Obj=super().save(*args,**kwargs)
            self.save()