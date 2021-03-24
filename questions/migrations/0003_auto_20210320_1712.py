# Generated by Django 3.1.7 on 2021-03-20 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_question_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.CharField(choices=[('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3'), ('MEOW', 'MEOW'), ('Gen Chem', 'Gen Chem'), ('EG', 'EG'), ('ES', 'ES'), ('PnS', 'PnS'), ('General', 'General')], default='9', max_length=20),
        ),
    ]
