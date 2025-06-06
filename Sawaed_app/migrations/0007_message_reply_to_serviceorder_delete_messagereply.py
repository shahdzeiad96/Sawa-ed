# Generated by Django 5.1.6 on 2025-04-10 08:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sawaed_app', '0006_messagereply'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Sawaed_app.message'),
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Sawaed_app.servicelisting')),
            ],
        ),
        migrations.DeleteModel(
            name='MessageReply',
        ),
    ]
