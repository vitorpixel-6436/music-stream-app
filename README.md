# Music Stream App

Django web application for music streaming and downloading with full metadata support.

## Features

- 🎵 Stream music directly from browser
- ⬇️ Download tracks
- 🏷️ Automatic metadata extraction (ID3, FLAC)
- 📊 Full music library management
- 🎨 Beautiful web interface
- 📱 Responsive design
- 🔍 Advanced search functionality
- 🎯 Playlist creation and management
- 📈 Play count tracking
- 🎭 Multi-format support (MP3, FLAC, OGG, M4A)

## Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript (Web Audio API)
- **Database**: SQLite/PostgreSQL
- **Audio Processing**: mutagen, ffmpeg
- **API**: Django REST Framework

## Project Structure

```
music-stream-app/
├── config/                 # Django configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── music/                  # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # Views and API endpoints
│   ├── urls.py            # URL routing
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin interface
│   ├── apps.py            # App configuration
│   ├── services/          # Business logic
│   │   ├── metadata_parser.py
│   │   ├── music_source_service.py
│   │   ├── player_service.py
│   │   └── playlist_service.py
│   ├── management/        # Custom commands
│   │   └── commands/
│   │       └── scan_library.py
│   ├── migrations/        # Database migrations
│   ├── templates/music/   # HTML templates
│   │   ├── base.html
│   │   ├── library.html
│   │   ├── player.html
│   │   ├── album_detail.html
│   │   ├── artist_detail.html
│   │   └── playlist_detail.html
│   └── templatetags/      # Custom template filters
│       └── music_filters.py
├── static/
│   ├── css/               # Stylesheets
│   │   ├── base.css
│   │   ├── player.css
│   │   └── library.css
│   ├── js/                # JavaScript
│   │   ├── player.js
│   │   ├── playlist.js
│   │   ├── search.js
│   │   └── waveform.js
│   └── icons/             # Icons and images
├── media/                 # User uploads
│   ├── tracks/
│   ├── covers/
│   └── avatars/
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.9+
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/music-stream-app.git
   cd music-stream-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

Access the application at `http://localhost:8000`

## Database Models

### Artist
- id (UUID)
- name (CharField)
- bio (TextField)
- photo (ImageField)
- created_at (DateTimeField)

### Album
- id (UUID)
- title (CharField)
- artist (ForeignKey to Artist)
- cover (ImageField)
- year (IntegerField)
- genre (CharField)
- created_at (DateTimeField)

### Track
- id (UUID)
- title (CharField)
- artist (ForeignKey to Artist)
- album (ForeignKey to Album)
- file (FileField)
- duration (IntegerField)
- bitrate (IntegerField)
- track_number (IntegerField)
- play_count (IntegerField)
- last_played (DateTimeField)
- created_at (DateTimeField)

### Playlist
- id (UUID)
- name (CharField)
- description (TextField)
- tracks (ManyToManyField through PlaylistTrack)
- cover (ImageField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

## API Endpoints

### Music Library
- `GET /api/library/` - Get all tracks, albums, artists
- `GET /api/tracks/` - List all tracks
- `GET /api/albums/` - List all albums
- `GET /api/artists/` - List all artists

### Streaming
- `GET /api/stream/<track_id>/` - Stream track with Range request support
- `POST /api/upload/` - Upload new track with metadata parsing

### Search
- `GET /api/search/?q=query` - Search across title, artist, album

### Playlists
- `GET /api/playlists/` - List all playlists
- `POST /api/playlists/` - Create new playlist
- `GET /api/playlists/<id>/` - Get playlist details
- `POST /api/playlists/<id>/tracks/` - Add track to playlist
- `DELETE /api/playlists/<id>/tracks/<track_id>/` - Remove track from playlist

## Configuration

Edit `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_NAME=music_stream.db
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=localhost

# Audio settings
MAX_UPLOAD_SIZE=50  # MB
SUPPORTED_FORMATS=mp3,flac,ogg,m4a
AUDIO_QUALITY=high

# Localization
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
```

## Running with Docker

```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000`

## Development

### Run tests
```bash
python manage.py test
```

### Lint code
```bash
flake8 .
pylint music/
```

### Format code
```bash
black .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

## Author

Created with ❤️ for music lovers
