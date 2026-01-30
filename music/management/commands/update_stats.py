"""Management command to update system statistics

Usage:
    python manage.py update_stats
    
This command updates the SystemSettings model with current statistics:
- Total tracks count
- Total plays count
- Total downloads count

Run this command periodically (e.g., via cron) to keep statistics up-to-date.
"""

from django.core.management.base import BaseCommand
from music.models import SystemSettings, MusicFile, Artist, Album, Genre
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Обновление статистики системы'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Показать детальную статистику'
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        
        self.stdout.write(
            self.style.HTTP_INFO('\n' + '='*60)
        )
        self.stdout.write(
            self.style.HTTP_INFO('📊 Music Stream App - Statistics Update')
        )
        self.stdout.write(
            self.style.HTTP_INFO('='*60 + '\n')
        )
        
        # Load settings
        settings = SystemSettings.load()
        
        # Store old values
        old_tracks = settings.total_tracks
        old_plays = settings.total_plays
        old_downloads = settings.total_downloads
        
        self.stdout.write(
            self.style.HTTP_INFO('⏳ Обновление статистики...')
        )
        
        # Update statistics
        settings.update_statistics()
        
        # Calculate changes
        tracks_change = settings.total_tracks - old_tracks
        plays_change = settings.total_plays - old_plays
        downloads_change = settings.total_downloads - old_downloads
        
        # Print results
        self.stdout.write('\n' + self.style.SUCCESS('✅ Статистика обновлена успешно!'))
        self.stdout.write('\n' + self.style.HTTP_INFO('📈 Основная статистика:'))
        
        self._print_stat_line(
            'Треков', 
            old_tracks, 
            settings.total_tracks, 
            tracks_change
        )
        self._print_stat_line(
            'Прослушиваний', 
            old_plays, 
            settings.total_plays, 
            plays_change
        )
        self._print_stat_line(
            'Скачиваний', 
            old_downloads, 
            settings.total_downloads, 
            downloads_change
        )
        
        if verbose:
            self._print_detailed_stats()
        
        self.stdout.write(
            self.style.HTTP_INFO('\n' + '='*60 + '\n')
        )
    
    def _print_stat_line(self, label, old_value, new_value, change):
        """Print a formatted statistics line with change indicator"""
        change_str = ''
        if change > 0:
            change_str = self.style.SUCCESS(f' (+{change:,})')
        elif change < 0:
            change_str = self.style.ERROR(f' ({change:,})')
        else:
            change_str = self.style.WARNING(' (без изменений)')
        
        self.stdout.write(
            f'   {label:20s} {old_value:>10,} → {new_value:>10,}{change_str}'
        )
    
    def _print_detailed_stats(self):
        """Print detailed system statistics"""
        self.stdout.write('\n' + self.style.HTTP_INFO('📊 Детальная статистика:'))
        
        # Artists
        artist_count = Artist.objects.count()
        self.stdout.write(f'   Исполнителей: {self.style.SUCCESS(f"{artist_count:,}")}')
        
        # Albums
        album_count = Album.objects.count()
        self.stdout.write(f'   Альбомов: {self.style.SUCCESS(f"{album_count:,}")}')
        
        # Genres
        genre_count = Genre.objects.count()
        self.stdout.write(f'   Жанров: {self.style.SUCCESS(f"{genre_count:,}")}')
        
        # Users
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_staff=True).count()
        self.stdout.write(
            f'   Пользователей: {self.style.SUCCESS(f"{user_count:,}")} '
            f'({admin_count} админов)'
        )
        
        # File formats breakdown
        self.stdout.write('\n' + self.style.HTTP_INFO('🎵 По форматам:'))
        formats = MusicFile.objects.values('format').distinct()
        for fmt in formats:
            format_name = fmt['format']
            count = MusicFile.objects.filter(format=format_name).count()
            self.stdout.write(
                f'   {format_name.upper():8s} {self.style.SUCCESS(f"{count:,} треков")}'
            )
        
        # Top artists by track count
        self.stdout.write('\n' + self.style.HTTP_INFO('⭐ Топ исполнителей:'))
        top_artists = Artist.objects.annotate(
            track_count=models.Count('tracks')
        ).order_by('-track_count')[:5]
        
        for i, artist in enumerate(top_artists, 1):
            self.stdout.write(
                f'   {i}. {artist.name[:40]:40s} '
                f'{self.style.SUCCESS(f"{artist.track_count:,} треков")}'
            )
