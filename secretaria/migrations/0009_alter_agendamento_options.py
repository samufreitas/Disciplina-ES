# Generated by Django 4.2.3 on 2023-09-12 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0008_alter_tipo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agendamento',
            options={'ordering': ['-data'], 'verbose_name': 'Agendamento', 'verbose_name_plural': 'Agendamentos'},
        ),
    ]