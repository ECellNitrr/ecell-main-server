# Generated by Django 3.0.5 on 2022-10-15 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='domain',
            field=models.CharField(choices=[['tech', 'tech'], ['spons', 'spons'], ['pr', 'pr'], ['doc', 'doc'], ['design', 'design'], ['em', 'em'], ['none', 'none']], default='pr', max_length=100),
        ),
    ]
