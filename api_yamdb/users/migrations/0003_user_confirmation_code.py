# Generated by Django 3.2 on 2023-02-28 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230228_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=50, null=True, verbose_name='Код'),
        ),
    ]