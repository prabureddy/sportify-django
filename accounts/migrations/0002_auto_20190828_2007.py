# Generated by Django 2.2 on 2019-08-28 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_no',
            field=models.IntegerField(blank=True, max_length=12, null=True),
        ),
    ]
