# Generated by Django 2.2.6 on 2019-10-18 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scraping', '0006_auto_20191018_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100, unique=True, verbose_name='E-mail')),
                ('password', models.CharField(max_length=100, verbose_name='Пароль')),
                ('is_active', models.BooleanField(default=True, verbose_name='Получать рассылку?')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.City', verbose_name='Город')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.Speciality', verbose_name='Специальность')),
            ],
            options={
                'verbose_name': 'Подписчик',
                'verbose_name_plural': 'Подписчики',
            },
        ),
    ]
