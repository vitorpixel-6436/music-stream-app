# Generated migration for v2.1.0 - Admin & Management QoL

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Music Stream App', max_length=100)),
                ('site_description', models.TextField(blank=True, default='Premium music streaming application')),
                ('max_upload_size', models.IntegerField(default=100, help_text='Max upload size in MB')),
                ('allowed_formats', models.CharField(
                    default='mp3,flac,wav,m4a,ogg',
                    help_text='Comma-separated list of allowed audio formats',
                    max_length=255
                )),
                ('allow_registration', models.BooleanField(default=True)),
                ('require_email_verification', models.BooleanField(default=False)),
                ('max_uploads_per_user', models.IntegerField(default=100, help_text='0 = unlimited')),
                ('auto_extract_metadata', models.BooleanField(default=True)),
                ('auto_generate_waveforms', models.BooleanField(default=False)),
                ('normalize_audio', models.BooleanField(default=False)),
                ('default_theme', models.CharField(
                    choices=[
                        ('glass', 'Apple Glass'),
                        ('steam', 'Steam Gaming'),
                        ('spotify', 'Spotify Minimal'),
                        ('msi', 'MSI Gaming')
                    ],
                    default='glass',
                    max_length=20
                )),
                ('enable_animations', models.BooleanField(default=True)),
                ('total_tracks', models.PositiveIntegerField(default=0, editable=False)),
                ('total_plays', models.PositiveIntegerField(default=0, editable=False)),
                ('total_downloads', models.PositiveIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'System Settings',
                'verbose_name_plural': 'System Settings',
            },
        ),
        migrations.CreateModel(
            name='UploadSession',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    primary_key=True,
                    serialize=False
                )),
                ('total_files', models.PositiveIntegerField(default=0)),
                ('successful_uploads', models.PositiveIntegerField(default=0)),
                ('failed_uploads', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('processing', 'Processing'),
                        ('completed', 'Completed'),
                        ('failed', 'Failed')
                    ],
                    default='pending',
                    max_length=20
                )),
                ('error_log', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='upload_sessions',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
