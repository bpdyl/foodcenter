# Generated by Django 3.1.7 on 2021-04-22 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0011_auto_20210417_0949'),
        ('core', '0006_auto_20210422_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
    ]
