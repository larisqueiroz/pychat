# Generated by Django 5.0.4 on 2024-08-20 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_img_base64_alter_message_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='img_base64',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
