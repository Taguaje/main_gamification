# Generated by Django 2.0.5 on 2018-05-31 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0010_auto_20180531_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameters',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.LMSEvents'),
        ),
    ]
