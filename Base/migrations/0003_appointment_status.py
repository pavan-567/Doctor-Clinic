# Generated by Django 4.1.10 on 2024-06-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_appointment_patientemail_appointment_patientname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('completed', 'completed')], default='pending', max_length=50),
        ),
    ]
