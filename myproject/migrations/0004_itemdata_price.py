# Generated by Django 4.2.6 on 2023-10-15 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0003_itemdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdata',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]