# Generated by Django 2.2 on 2019-10-18 05:14

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_codeforcoder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=30, validators=[django.core.validators.MinLengthValidator(4)])),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(default='', max_length=250)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Contact CodeForCoder',
            },
        ),
    ]
