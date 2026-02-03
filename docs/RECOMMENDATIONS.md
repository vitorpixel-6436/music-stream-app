# 🎵 ML Recommendation Engine Documentation

**Version:** v1.3.0  
**Status:** ✅ Production Ready

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Backend API](#backend-api)
4. [Frontend Integration](#frontend-integration)
5. [Usage Examples](#usage-examples)
6. [Customization](#customization)
7. [Performance](#performance)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Music Stream App включает мощный ML-движок рекомендаций, основанный на:

- **Content-Based Filtering** - Рекомендации на основе характеристик треков
- **Collaborative Filtering** - Упрощённый анализ поведения пользователей
- **Hybrid Approach** - Комбинация нескольких алгоритмов

### ✨ Особенности:

- ✅ **Без внешних ML библиотек** (sklearn не требуется)
- ✅ **Быстрое выполнение** (<100ms на запрос)
- ✅ **Кэширование** (1 час по умолчанию)
- ✅ **REST API** (JSON responses)
- ✅ **Beautiful UI** (Steam UI компоненты)

---

## 🏗️ Architecture

### Backend Components:

```
music/
├── recommendations.py          # ML движок
├── recommendation_views.py     # REST API views
├── models.py                   # ListeningHistory model
└── urls.py                     # API routes
```

### Frontend Components:

```
music/static/music/
├── js/
│   └── recommendations.js      # JS API client
└── css/
    └── recommendations.css     # Carousel styles
```

### Data Flow:

```
User Action → Record Play → ListeningHistory DB
                                    ↓
                          ML Recommendation Engine
                                    ↓
                          Personalized Results
                                    ↓
                          REST API → Frontend
                                    ↓
                          Beautiful Carousel UI
```

---

## 🔌 Backend API

### Endpoints:

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/recommendations/` | GET | ✅ | Персональные рекомендации |
| `/api/track/<id>/similar/` | GET | ❌ | Похожие треки |
| `/api/charts/` | GET | ❌ | Топ-чарты |
| `/api/continue-listening/` | GET | ✅ | Продолжить прослушивание |
| `/api/track/<id>/play/` | POST | ✅ | Записать прослушивание |
| `/api/listening-stats/` | GET | ✅ | Статистика пользователя |
| `/api/recent-plays/` | GET | ✅ | Недавние прослушивания |

---

### 1. Personalized Recommendations

**Endpoint:** `GET /music/api/recommendations/`

**Query Parameters:**
- `limit` (int, optional) - Количество рекомендаций (default: 20, max: 50)

**Response:**
```json
{
  "status": "success",
  "recommendations": [
    {
      "id": "uuid",
      "title": "Song Name",
      "artist": {
        "id": "uuid",
        "name": "Artist Name"
      },
      "duration": 180,
      "play_count": 1234,
      "cover_url": "/media/covers/...",
      "format": "mp3"
    }
  ],
  "count": 20,
  "user": "username"
}
```

**Example:**
```bash
curl http://localhost:8000/music/api/recommendations/?limit=10 \
  -H "Authorization: Bearer <token>"
```

---

### 2. Similar Tracks

**Endpoint:** `GET /music/api/track/<track_id>/similar/`

**Query Parameters:**
- `limit` (int, optional) - Количество похожих треков (default: 10, max: 30)

**Response:**
```json
{
  "status": "success",
  "original_track": { /* track object */ },
  "similar": [ /* array of track objects */ ],
  "count": 10
}
```

**Example:**
```bash
curl http://localhost:8000/music/api/track/abc123-def456/similar/?limit=5
```

---

### 3. Top Charts

**Endpoint:** `GET /music/api/charts/`

**Query Parameters:**
- `period` (string, optional) - 'weekly' или 'monthly' (default: 'weekly')
- `limit` (int, optional) - Количество треков (default: 20, max: 50)

**Response:**
```json
{
  "status": "success",
  "charts": [ /* array of track objects */ ],
  "count": 20,
  "period": "weekly",
  "period_days": 7
}
```

**Example:**
```bash
curl "http://localhost:8000/music/api/charts/?period=monthly&limit=30"
```

---

### 4. Record Play

**Endpoint:** `POST /music/api/track/<track_id>/play/`

**Request Body:**
```json
{
  "duration": 180,
  "position": 180,
  "source": "playlist",
  "device": "web"
}
```

**Response:**
```json
{
  "status": "success",
  "play_id": "uuid",
  "completion_percentage": 100,
  "message": "Play recorded successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/music/api/track/abc123/play/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <token>" \
  -d '{"duration": 180, "position": 180}'
```

---

## 🎨 Frontend Integration

### Quick Start:

**1. Include CSS & JS:**

```html
<!-- In your template -->
<link rel="stylesheet" href="{% static 'music/css/recommendations.css' %}">
<script src="{% static 'music/js/recommendations.js' %}"></script>
```

**2. Create Container:**

```html
<div id="personalized-recommendations"></div>
```

**3. Load Recommendations:**

```javascript
// Wait for page load
document.addEventListener('DOMContentLoaded', async () => {
    const manager = window.recommendationManager;
    
    // Get recommendations
    const tracks = await manager.getPersonalized(20);
    
    // Render carousel
    const container = document.getElementById('personalized-recommendations');
    manager.renderCarousel(tracks, container, 'Recommended for You');
});
```

---

## 💡 Usage Examples

### Example 1: Personalized Recommendations

```javascript
const manager = new RecommendationManager();

// Fetch personalized recommendations
const recommendations = await manager.getPersonalized(20);

// Render in container
const container = document.getElementById('recs');
manager.renderCarousel(
    recommendations, 
    container, 
    '🎵 Recommended for You'
);
```

---

### Example 2: Similar Tracks Page

```javascript
// On track detail page
const trackId = 'abc123-def456';
const manager = new RecommendationManager();

// Get similar tracks
const similar = await manager.getSimilarTracks(trackId, 10);

// Render
const container = document.getElementById('similar-tracks');
manager.renderCarousel(
    similar, 
    container, 
    'Similar Tracks'
);
```

---

### Example 3: Top Charts Widget

```javascript
const manager = new RecommendationManager();

// Get weekly top charts
const charts = await manager.getTopCharts('weekly', 20);

// Render
const container = document.getElementById('top-charts');
manager.renderCarousel(
    charts, 
    container, 
    '🔥 Top Charts This Week'
);
```

---

### Example 4: Continue Listening

```javascript
const manager = new RecommendationManager();

// Get tracks to continue
const tracks = await manager.getContinueListening(10);

// Render
const container = document.getElementById('continue-listening');
manager.renderCarousel(
    tracks, 
    container, 
    '▶️ Continue Listening'
);
```

---

### Example 5: Track Play Recording

```javascript
const manager = new RecommendationManager();
const trackId = 'abc123';

// Record play when track ends
audioPlayer.addEventListener('ended', async () => {
    await manager.recordPlay(trackId, {
        duration: audioPlayer.duration,
        position: audioPlayer.currentTime,
        source: 'player',
        device: 'web'
    });
});
```

---

## ⚙️ Customization

### Backend:

**Adjust Cache Timeout:**

```python
# In recommendation_views.py
engine = RecommendationEngine(cache_timeout=7200)  # 2 hours
```

**Custom Similarity Weights:**

```python
# In recommendations.py, RecommendationEngine.get_similar_tracks()
# Adjust weights:
score = 0.5 * genre_match + 0.3 * artist_match + 0.2 * title_similarity
```

### Frontend:

**Custom Card Rendering:**

```javascript
class CustomRecommendationManager extends RecommendationManager {
    _renderTrackCard(track) {
        // Your custom card HTML
        return `<div class="custom-card">...</div>`;
    }
}
```

**Change Cache Duration:**

```javascript
const manager = new RecommendationManager();
manager.cacheDuration = 7200000; // 2 hours
```

---

## 🚀 Performance

### Optimization Tips:

**1. Use Caching:**
- Backend: Django cache (Redis recommended)
- Frontend: Browser memory cache (built-in)

**2. Limit Results:**
```javascript
// Don't fetch too many at once
const tracks = await manager.getPersonalized(10); // Good
const tracks = await manager.getPersonalized(100); // Bad
```

**3. Lazy Load Carousels:**
```javascript
// Load only when visible
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        loadRecommendations();
    }
});
observer.observe(container);
```

**4. Batch API Calls:**
```javascript
// Load multiple carousels in parallel
const [personalized, charts] = await Promise.all([
    manager.getPersonalized(10),
    manager.getTopCharts('weekly', 10)
]);
```

---

## 🐛 Troubleshooting

### Problem: No recommendations returned

**Solution:**
- Убедитесь, что у пользователя есть история прослушиваний
- Проверьте, что в БД есть треки
- Проверьте логи Django: `python manage.py runserver`

---

### Problem: 403 Forbidden on API calls

**Solution:**
- Убедитесь, что пользователь авторизован (для protected endpoints)
- Проверьте CSRF token для POST запросов

---

### Problem: Carousel not displaying

**Solution:**
```javascript
// Check if manager initialized
console.log(window.recommendationManager);

// Check if tracks loaded
const tracks = await manager.getPersonalized(10);
console.log(tracks);

// Check console for errors
```

---

## 📚 Additional Resources

- [API Reference](RECOMMENDATION_API.md)
- [Algorithm Details](RECOMMENDATION_ALGORITHMS.md)
- [Steam UI Framework](../steam_ui/README.md)

---

**Made with ❤️ by Music Stream App Team**
