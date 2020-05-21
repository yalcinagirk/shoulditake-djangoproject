# Generated by Django 3.0.6 on 2020-05-17 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Hakkımda')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Profil Fotoğrafı')),
                ('dogum_tarihi', models.DateField(blank=True, null=True, verbose_name='Doğum Tarihi')),
                ('cinsiyet', models.CharField(choices=[(None, 'Cinsiyet'), ('diger', 'DİĞER'), ('erkek', 'ERKEK'), ('kadın', 'KADIN')], max_length=6, verbose_name='Cinsiyet')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Kullanici Profilleri',
            },
        ),
    ]
