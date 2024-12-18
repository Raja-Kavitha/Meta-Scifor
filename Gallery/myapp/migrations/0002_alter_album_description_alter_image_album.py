# Generated by Django 4.2.4 on 2024-12-05 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='album',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='myapp.album'),
        ),
    ]
