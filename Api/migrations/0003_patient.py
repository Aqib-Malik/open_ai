# Generated by Django 4.2 on 2023-04-30 07:16

import Api.models.user
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0002_hospital_permission_role_user_role_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('patient_name', models.CharField(max_length=100)),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'A-'), ('O+', 'O-'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3, null=True)),
                ('patient_dob', models.DateField(blank=True, null=True)),
                ('relation', models.CharField(blank=True, choices=[('Self', 'Self'), ('Father', 'Father'), ('Mother', 'Mother'), ('Husband', 'Husband'), ('Wife', 'Wife'), ('Grand Father', 'Grand Father'), ('Grand Mother', 'Grand Mother'), ('Nephew', 'Nephew'), ('Niece', 'Niece'), ('Cousin', 'Cousin'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt'), ('Son', 'Son'), ('Daughter', 'Daughter'), ('Brother', 'Brother'), ('Sister', 'Sister'), ('Other', 'Other')], max_length=12, null=True)),
                ('mr_number', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('others', 'others')], default='male', max_length=10)),
                ('profile_image', models.ImageField(blank=True, default=Api.models.user.get_default_profile_image_path, max_length=255, null=True, upload_to=Api.models.user.get_profile_image_path)),
                ('cards_printed', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='Api.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api.user')),
            ],
            options={
                'unique_together': {('user', 'patient_name', 'relation', 'deleted')},
            },
        ),
    ]