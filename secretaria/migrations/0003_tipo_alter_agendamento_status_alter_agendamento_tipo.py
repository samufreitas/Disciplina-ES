# Generated by Django 4.2.3 on 2023-08-10 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0002_alter_agendamento_opicional_alter_agendamento_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo',
                'verbose_name_plural': 'Tipos',
                'ordering': ['id'],
            },
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='status',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='secretaria.tipo'),
        ),
    ]
