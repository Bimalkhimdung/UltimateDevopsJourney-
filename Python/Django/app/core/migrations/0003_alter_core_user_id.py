# Generated by Django 4.2.16 on 2024-11-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_core_id_core_email_core_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='core',
            name='user_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
