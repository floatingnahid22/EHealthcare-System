# Generated by Django 3.2.6 on 2021-08-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcareApp', '0009_alter_patientinfo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='doctorsPP/'),
        ),
    ]
