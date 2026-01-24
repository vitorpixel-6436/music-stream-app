# Music Stream App - Deployment Guide

Comprehensive guide for deploying the Music Streaming Application in development, staging, and production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Management](#database-management)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Docker & Docker Compose**: Version 3.8+
- **Python**: 3.11+ (for local development)
- **PostgreSQL**: 15+ (managed by Docker)
- **Redis**: 7+ (managed by Docker)
- **Nginx**: Latest (managed by Docker)
- **Disk Space**: Minimum 20GB for media files
- **RAM**: Minimum 4GB
- **CPU**: Minimum 2 cores

### Required Packages

```bash
pip install django django-cors-headers pillow gunicorn psycopg2-binary redis
```

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
```

### 2. Create Environment File

Create `.env` file in the project root:

```bash
# Django Settings
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,*.local

# Database
POSTGRES_DB=music_stream
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PORT=6379

# Email (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### 3. Run Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver 0.0.0.0:8000
```

Access the application at `http://localhost:8000`

## Docker Deployment

### Quick Start (Development)

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f web
```

### Production Deployment with Docker

```bash
# Create production environment file
cp .env.example .env.production

# Edit for production settings
nano .env.production

# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Verify all services are running
docker-compose -f docker-compose.prod.yml ps
```

## Production Deployment

### Option 1: AWS EC2

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo amazon-linux-extras install docker
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

# Clone and deploy
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
docker-compose up -d
```

### Option 2: DigitalOcean

```bash
# SSH into your droplet
ssh root@your-droplet-ip

# Install Docker using script
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Deploy application
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
docker-compose up -d
```

### Option 3: Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login and create app
heroku login
heroku create music-stream-app

# Deploy
git push heroku main
```

## Environment Configuration

### Production Environment Variables

```bash
# Security (CRITICAL)
DEBUG=0
SECRET_KEY=generate-a-secure-random-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Security Headers
SECURE_SSL_REDIRECT=1
SESSION_COOKIE_SECURE=1
CSRF_COOKIE_SECURE=1
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=1

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://user:password@host:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=app-specific-password

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/music-stream/app.log
```

## Database Management

### Backup Database

```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U postgres music_stream > backup.sql

# Backup with timestamp
docker-compose exec db pg_dump -U postgres music_stream > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database

```bash
# Restore from backup
docker-compose exec -T db psql -U postgres music_stream < backup.sql
```

### Run Migrations

```bash
# Apply migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Check migration status
docker-compose exec web python manage.py showmigrations
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check all services
curl http://localhost/health/

# Check database
docker-compose exec db pg_isready -U postgres

# Check Redis
docker-compose exec redis redis-cli ping
```

### View Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# View last 100 lines
docker-compose logs --tail=100 web
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build --no-cache

# Restart services
docker-compose up -d

# Clear cache
docker-compose exec web python manage.py clear_cache
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error

```bash
# Check database service
docker-compose ps db

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

#### 2. Permission Denied Error

```bash
# Fix media directory permissions
sudo chown -R 1000:1000 ./media
sudo chmod -R 755 ./media
```

#### 3. Static Files Not Loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Restart nginx
docker-compose restart nginx
```

#### 4. Redis Connection Issues

```bash
# Check Redis connection
docker-compose exec redis redis-cli ping

# Flush Redis (caution!)
docker-compose exec redis redis-cli FLUSHALL
```

#### 5. High Memory Usage

```bash
# Check container resource usage
docker stats

# Reduce worker count in docker-compose.yml
# Update the --workers parameter in the web service
```

### Accessing Container Shell

```bash
# Access Django container
docker-compose exec web bash

# Access PostgreSQL container
docker-compose exec db psql -U postgres

# Access Redis container
docker-compose exec redis redis-cli
```

## Performance Optimization

### Database Optimization

```bash
# Create database indexes
docker-compose exec web python manage.py create_indexes

# Analyze query performance
docker-compose exec db psql -U postgres -c "ANALYZE music_stream"
```

### Cache Optimization

```bash
# Monitor cache hits/misses
docker-compose exec redis redis-cli INFO stats

# Configure cache timeout in settings.py
CACHE_TIMEOUT = 3600  # 1 hour
```

## Security Hardening

1. **Change Default Passwords**: Always change default database and Redis passwords
2. **Enable HTTPS**: Use Let's Encrypt for free SSL certificates
3. **Configure Firewall**: Only allow necessary ports (80, 443)
4. **Regular Updates**: Keep Docker images and dependencies updated
5. **Backup Strategy**: Regular automated backups to secure storage
6. **Monitor Logs**: Set up log aggregation for security auditing

## Support and Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## License

This deployment guide is part of the Music Stream App project.
