# Generated by Django 4.0.4 on 2022-05-02 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_gen', '0009_questionsequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='questions',
            field=models.ManyToManyField(to='mcq_gen.question'),
        ),
    ]