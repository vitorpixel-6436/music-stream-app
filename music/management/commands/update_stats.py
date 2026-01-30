from django.core.management.base import BaseCommand
from music.models import SystemSettings


class Command(BaseCommand):
    help = 'Обновление статистики системы'

    def handle(self, *args, **options):
        settings = SystemSettings.load()
        
        self.stdout.write('Обновление статистики...')
        
        old_tracks = settings.total_tracks
        old_plays = settings.total_plays
        old_downloads = settings.total_downloads
        
        settings.update_statistics()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Статистика обновлена:'))
        self.stdout.write(f'Треков: {old_tracks} → {settings.total_tracks}')
        self.stdout.write(f'Прослушиваний: {old_plays:,} → {settings.total_plays:,}')
        self.stdout.write(f'Скачиваний: {old_downloads:,} → {settings.total_downloads:,}')
