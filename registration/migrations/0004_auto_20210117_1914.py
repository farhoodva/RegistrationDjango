# Generated by Django 3.1.3 on 2021-01-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_driverinfo_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverinfo',
            name='national_id',
            field=models.CharField(error_messages={'unique': 'این کد ملی قبلا ثبت شده است'}, max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='کد ملی'),
        ),
        migrations.AlterField(
            model_name='driverinfo',
            name='smart_card_number',
            field=models.CharField(error_messages={'unique': 'این کارت هوشمند قبلا ثبت شده است'}, max_length=5, unique=True, verbose_name='شماره کارت هوشمند'),
        ),
    ]
