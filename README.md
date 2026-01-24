# Music Streaming Application 🎵

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.0+-darkgreen.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-latest-blue.svg)](https://www.docker.com/)

A professional-grade web application for streaming and downloading music with full metadata support, advanced search capabilities, and responsive design.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Performance Optimization](#performance-optimization)
- [Security Features](#security-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

### 🎵 Core Music Features

- **Stream Music** - Listen to music directly in your browser with high-quality audio
- **Download Tracks** - Save music files to your device for offline playback
- **Multiple Format Support** - MP3, FLAC, WAV, AAC, OGG
- **High Quality Streaming** - Up to 128 kbps audio quality
- **Format Conversion** - Automatic conversion between supported formats
- **Metadata Management** - Complete ID3 tag support and metadata extraction

### 🔍 Discovery & Organization

- **Advanced Search** - Search by track title, artist, or album name
- **Smart Filtering** - Filter music by artist, album, or genre
- **Genre Classification** - Organize music by musical styles
- **Album Grouping** - Browse music organized by albums
- **Artist Information** - Full artist details with biography
- **Smart Playlists** - Create and manage custom playlists
- **Favorites System** - Mark your favorite tracks for quick access
- **Play Count Tracking** - Automatic tracking of listening statistics

### 🎨 User Experience

- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Modern UI** - Beautiful glassmorphism design with smooth animations
- **Pagination** - Efficient content loading with 12 items per page
- **Autocomplete Search** - Real-time search suggestions
- **Sort Options** - Multiple sorting methods (date, title, popularity)
- **Health Checks** - Automated service health monitoring
- **Dark Theme** - Easy on the eyes design

### 📊 Advanced Features

- **Usage Statistics** - Track play counts and download history
- **Download Tracking** - Monitor download activity and usage patterns
- **Error Handling** - Comprehensive error pages and recovery
- **Logging System** - Detailed application logging for debugging
- **Caching Layer** - Redis-based caching for performance
- **Database Optimization** - Indexed queries for fast retrieval

## Tech Stack

### Backend

- **Framework**: Django 4.0+
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ASGI Server**: Gunicorn 4 workers
- **Language**: Python 3.11+

### Frontend

- **HTML5**: Modern semantic HTML
- **CSS3**: Glassmorphism design with animations
- **JavaScript**: Modern vanilla JS with no frameworks
- **Responsive**: Mobile-first approach

### Infrastructure

- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx reverse proxy
- **Version Control**: Git
- **CI/CD Ready**: GitHub Actions compatible

## Quick Start

### Prerequisites

- Docker & Docker Compose 3.8+
- Git
- 4GB+ RAM
- 20GB+ disk space

### Start Application

```bash
# Clone the repository
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app

# Create environment file
cp .env.example .env

# Start with Docker
docker-compose up -d

# Access the application
# Web: http://localhost:80
# Admin: http://localhost/admin
```

## Installation

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver 0.0.0.0:8000
```

### Production Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed production setup instructions.

## Docker Deployment

### Development

```bash
docker-compose up -d
```

### Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Configuration

### Environment Variables

Create `.env` file with the following variables:

```bash
# Security
DEBUG=0
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com

# Database
POSTGRES_DB=music_stream
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure-password

# Redis
REDIS_URL=redis://redis:6379/0

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

## API Endpoints

### Music

- `GET /` - Home page with music list
- `GET /api/music/<id>/` - Get music details
- `GET /api/music/<id>/stream/` - Stream music file
- `GET /api/music/<id>/download/` - Download music file
- `POST /api/music/upload/` - Upload new music

### Search & Filter

- `GET /?q=query` - Search music
- `GET /?artist=artist_id` - Filter by artist
- `GET /?album=album_id` - Filter by album
- `GET /?sort=field` - Sort results
- `GET /api/search/?q=query` - Autocomplete search

## Database Schema

### Main Tables

- **MusicFile**: Audio file records with metadata
- **Artist**: Artist information and details
- **Album**: Album metadata and grouping
- **UserFavorite**: User's favorite tracks
- **PlayHistory**: User playback statistics

## Performance Optimization

### Caching Strategy

- Database query caching (1 hour TTL)
- Static file caching (browser cache)
- API response caching

### Database Optimization

- Indexed searches on title, artist
- Pagination for large result sets
- Query optimization with select_related

## Security Features

- **HTTPS/SSL**: Automatic redirect in production
- **CSRF Protection**: Built-in Django CSRF tokens
- **XSS Prevention**: Template auto-escaping
- **SQL Injection Prevention**: ORM parameterized queries
- **Rate Limiting**: Configurable rate limits
- **Security Headers**: HSTS, CSP, X-Frame-Options
- **Non-root Container**: Docker security best practice
- **Health Checks**: Continuous service monitoring

## Troubleshooting

### Database Connection Issues

```bash
docker-compose restart db
docker-compose logs db
```

### Static Files Not Loading

```bash
docker-compose exec web python manage.py collectstatic --noinput --clear
docker-compose restart nginx
```

### High Memory Usage

Reduce worker count in docker-compose.yml

### Permission Errors

```bash
sudo chown -R 1000:1000 ./media
sudo chmod -R 755 ./media
```

## Project Structure

```
music-stream-app/
├── config/              # Django configuration
├── music/              # Main app
│   ├── models.py       # Database models
│   ├── views.py        # View logic with search/filter
│   ├── urls.py         # URL routing
│   ├── forms.py        # Form handling with validation
│   ├── static/         # Static files (CSS, JS)
│   └── templates/      # HTML templates
├── docker-compose.yml  # Docker orchestration
├── Dockerfile          # Multi-stage build
├── requirements.txt    # Python dependencies
├── manage.py          # Django CLI
└── README.md          # This file
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

- Open an issue on GitHub
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment help
- Review [PROJECT_STATUS.md](PROJECT_STATUS.md) for project roadmap

## Acknowledgments

Built with Django, PostgreSQL, Redis, Docker, and Nginx.

---

**Made with ❤️ by vitorpixel-6436**
