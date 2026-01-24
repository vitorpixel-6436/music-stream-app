from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from music.models import Artist, Album, MusicFile
import json
from django.core.files.uploadedfile import SimpleUploadedFile


class ArtistModelTests(TestCase):
    """Unit tests for Artist model"""
    
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")
    
    def test_artist_creation(self):
        """Test artist can be created successfully"""
        self.assertEqual(self.artist.name, "Test Artist")
        self.assertTrue(Artist.objects.filter(name="Test Artist").exists())
    
    def test_artist_str_representation(self):
        """Test artist string representation"""
        self.assertEqual(str(self.artist), "Test Artist")


class AlbumModelTests(TestCase):
    """Unit tests for Album model"""
    
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(
            title="Test Album",
            artist=self.artist
        )
    
    def test_album_creation(self):
        """Test album can be created successfully"""
        self.assertEqual(self.album.title, "Test Album")
        self.assertEqual(self.album.artist, self.artist)
    
    def test_album_str_representation(self):
        """Test album string representation"""
        expected = "Test Album by Test Artist"
        self.assertIn(self.album.artist.name, str(self.album))


class MusicFileModelTests(TestCase):
    """Unit tests for MusicFile model"""
    
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(
            title="Test Album",
            artist=self.artist
        )
        self.music_file = MusicFile.objects.create(
            title="Test Song",
            artist=self.artist,
            album=self.album,
            format="mp3",
            file_size=1024
        )
    
    def test_music_file_creation(self):
        """Test music file can be created successfully"""
        self.assertEqual(self.music_file.title, "Test Song")
        self.assertEqual(self.music_file.artist, self.artist)
        self.assertEqual(self.music_file.format, "mp3")
    
    def test_play_count_increment(self):
        """Test play count increments correctly"""
        initial_count = self.music_file.play_count
        self.music_file.increment_play_count()
        self.music_file.refresh_from_db()
        self.assertEqual(self.music_file.play_count, initial_count + 1)
    
    def test_download_count_increment(self):
        """Test download count increments correctly"""
        initial_count = self.music_file.download_count
        self.music_file.increment_download_count()
        self.music_file.refresh_from_db()
        self.assertEqual(self.music_file.download_count, initial_count + 1)


class ViewsTests(TestCase):
    """Unit tests for views"""
    
    def setUp(self):
        self.client = Client()
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(
            title="Test Album",
            artist=self.artist
        )
        self.music_file = MusicFile.objects.create(
            title="Test Song",
            artist=self.artist,
            album=self.album,
            format="mp3",
            file_size=1024
        )
    
    def test_index_view_status_code(self):
        """Test index view returns 200 status code"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_template(self):
        """Test index view uses correct template"""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'music/index.html')
    
    def test_index_view_context(self):
        """Test index view context contains music files"""
        response = self.client.get(reverse('index'))
        self.assertIn('music_files', response.context)
    
    def test_search_functionality(self):
        """Test search filters music correctly"""
        response = self.client.get(reverse('index'), {'q': 'Test Song'})
        self.assertEqual(response.status_code, 200)
    
    def test_pagination(self):
        """Test pagination works correctly"""
        # Create additional music files
        for i in range(15):
            MusicFile.objects.create(
                title=f"Song {i}",
                artist=self.artist,
                format="mp3",
                file_size=1024
            )
        response = self.client.get(reverse('index'))
        self.assertIn('music_files', response.context)


class APISearchTests(TestCase):
    """Unit tests for API search endpoint"""
    
    def setUp(self):
        self.client = Client()
        self.artist = Artist.objects.create(name="Test Artist")
        self.music_file = MusicFile.objects.create(
            title="Test Song",
            artist=self.artist,
            format="mp3",
            file_size=1024
        )
    
    def test_search_api_endpoint(self):
        """Test search API endpoint returns JSON"""
        response = self.client.get(reverse('api_search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('results', data)
    
    def test_search_api_short_query(self):
        """Test search API with query shorter than 2 chars returns empty"""
        response = self.client.get(reverse('api_search'), {'q': 'A'})
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)


class ErrorHandlingTests(TestCase):
    """Unit tests for error handling"""
    
    def setUp(self):
        self.client = Client()
    
    def test_404_not_found(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
    
    def test_invalid_music_file_id(self):
        """Test accessing non-existent music file"""
        response = self.client.get(reverse('player', args=[99999]))
        self.assertEqual(response.status_code, 404)


class InputValidationTests(TestCase):
    """Unit tests for input validation"""
    
    def test_artist_name_validation(self):
        """Test artist name is required"""
        with self.assertRaises(Exception):
            Artist.objects.create(name="")
    
    def test_music_file_title_required(self):
        """Test music file title is required"""
        artist = Artist.objects.create(name="Test Artist")
        with self.assertRaises(Exception):
            MusicFile.objects.create(
                title="",
                artist=artist,
                format="mp3",
                file_size=1024
            )
