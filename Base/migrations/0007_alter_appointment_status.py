# Generated by Django 4.1.10 on 2024-06-10 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0006_alter_doctor_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('processing', 'processing'), ('completed', 'completed')], default='pending', max_length=50),
        ),
    ]
