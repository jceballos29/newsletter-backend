# Generated by Django 3.2.9 on 2021-11-25 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0003_auto_20211125_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
