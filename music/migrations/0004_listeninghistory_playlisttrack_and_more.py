# Generated migration for Playlist tracks with through model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0003_unified_models'),
    ]

    operations = [
        # ====================================================================
        # STEP 1: Create ListeningHistory model
        # ====================================================================
        migrations.CreateModel(
            name='ListeningHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('played_at', models.DateTimeField(auto_now_add=True)),
                ('duration_listened', models.IntegerField(default=0, help_text='Duration listened in seconds')),
                ('completed', models.BooleanField(default=False)),
                ('session_id', models.UUIDField(blank=True, help_text='Session identifier for grouping', null=True)),
            ],
            options={
                'verbose_name': 'Listening History',
                'verbose_name_plural': 'Listening History',
                'ordering': ['-played_at'],
                'indexes': [],
            },
        ),
        
        # ====================================================================
        # STEP 2: Create PlaylistTrack model (through model)
        # ====================================================================
        migrations.CreateModel(
            name='PlaylistTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['position'],
                'indexes': [],
            },
        ),
        
        # ====================================================================
        # STEP 3: Update Playlist model (add new fields)
        # ====================================================================
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='playlist',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='playlists/covers/'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='is_collaborative',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playlist',
            name='total_duration',
            field=models.IntegerField(default=0, help_text='Total duration in seconds'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='track_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playlist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        
        # ====================================================================
        # STEP 4: Update DownloadTask indexes
        # ====================================================================
        migrations.RenameIndex(
            model_name='downloadtask',
            new_name='music_downl_user_id_33f7e9_idx',
            old_name='music_downl_user_id_f8a5e1_idx',
        ),
        migrations.RenameIndex(
            model_name='downloadtask',
            new_name='music_downl_status_504bbd_idx',
            old_name='music_downl_status_c9d4a2_idx',
        ),
        
        # ====================================================================
        # STEP 5: Update MusicFile indexes
        # ====================================================================
        migrations.RenameIndex(
            model_name='musicfile',
            new_name='music_music_artist__476a2b_idx',
            old_name='music_music_artist_title_idx',
        ),
        
        # ====================================================================
        # STEP 6: Alter existing fields
        # ====================================================================
        migrations.AlterField(
            model_name='favorite',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='musicfile',
            name='file',
            field=models.FileField(upload_to='music/'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='is_public',
            field=models.BooleanField(default=False, help_text='Whether this playlist is visible to other users'),
        ),
        
        # ====================================================================
        # STEP 7: CRITICAL - Remove old tracks field WITHOUT through
        # ====================================================================
        migrations.RemoveField(
            model_name='playlist',
            name='tracks',
        ),
        
        # ====================================================================
        # STEP 8: Add foreign keys to ListeningHistory
        # ====================================================================
        migrations.AddField(
            model_name='listeninghistory',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_history', to='music.musicfile'),
        ),
        migrations.AddField(
            model_name='listeninghistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_history', to=settings.AUTH_USER_MODEL),
        ),
        
        # ====================================================================
        # STEP 9: Add foreign keys to PlaylistTrack
        # ====================================================================
        migrations.AddField(
            model_name='playlisttrack',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlisttrack',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.playlist'),
        ),
        migrations.AddField(
            model_name='playlisttrack',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.musicfile'),
        ),
        
        # ====================================================================
        # STEP 10: Add NEW tracks field WITH through=PlaylistTrack
        # ====================================================================
        migrations.AddField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(
                related_name='playlists',
                through='music.PlaylistTrack',
                to='music.musicfile'
            ),
        ),
        
        # ====================================================================
        # STEP 11: Add indexes to Playlist
        # ====================================================================
        migrations.AddIndex(
            model_name='playlist',
            index=models.Index(fields=['user', '-updated_at'], name='music_playl_user_id_ab4a82_idx'),
        ),
        migrations.AddIndex(
            model_name='playlist',
            index=models.Index(fields=['is_public', '-updated_at'], name='music_playl_is_publ_ef1ee5_idx'),
        ),
        
        # ====================================================================
        # STEP 12: Add indexes to ListeningHistory
        # ====================================================================
        migrations.AddIndex(
            model_name='listeninghistory',
            index=models.Index(fields=['user', '-played_at'], name='music_liste_user_id_9e039b_idx'),
        ),
        migrations.AddIndex(
            model_name='listeninghistory',
            index=models.Index(fields=['track', '-played_at'], name='music_liste_track_i_c99f29_idx'),
        ),
        migrations.AddIndex(
            model_name='listeninghistory',
            index=models.Index(fields=['user', 'track', '-played_at'], name='music_liste_user_id_6ead05_idx'),
        ),
        migrations.AddIndex(
            model_name='listeninghistory',
            index=models.Index(fields=['-played_at'], name='music_liste_played__69f900_idx'),
        ),
        
        # ====================================================================
        # STEP 13: Add indexes to PlaylistTrack
        # ====================================================================
        migrations.AddIndex(
            model_name='playlisttrack',
            index=models.Index(fields=['playlist', 'position'], name='music_playl_playlis_407db8_idx'),
        ),
        
        # ====================================================================
        # STEP 14: Add unique constraint to PlaylistTrack
        # ====================================================================
        migrations.AlterUniqueTogether(
            name='playlisttrack',
            unique_together={('playlist', 'track')},
        ),
    ]
