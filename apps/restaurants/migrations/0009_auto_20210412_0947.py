# Generated by Django 3.1.7 on 2021-04-12 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0008_auto_20210408_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featured',
            name='restaurant',
            field=models.OneToOneField(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='featured', to='restaurants.restaurant'),
        ),
    ]
