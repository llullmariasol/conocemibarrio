# Generated by Django 4.0.2 on 2022-06-09 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neighborhood', '0007_neighborhoodimage_pointofinterest_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointofinterest',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]