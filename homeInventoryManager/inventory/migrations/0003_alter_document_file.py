# Generated by Django 3.2.15 on 2022-09-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20210704_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='docs/'),
        ),
    ]
