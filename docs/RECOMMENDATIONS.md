# 🤖 Recommendation Engine Documentation

**Version:** 1.3.0  
**Status:** ✅ Production Ready  
**Dependencies:** None (Pure Python + Django ORM)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Algorithms](#algorithms)
4. [API Reference](#api-reference)
5. [Frontend Integration](#frontend-integration)
6. [Data Models](#data-models)
7. [Performance](#performance)
8. [Examples](#examples)

---

## 🎯 Overview

The **Recommendation Engine** is a lightweight ML-powered music recommendation system built without external dependencies. It uses:

- **Content-based filtering** (genre, artist, text similarity)
- **Collaborative filtering** (simplified user behavior)
- **TF-IDF + Cosine similarity** (pure Python)
- **Django ORM optimization** for fast queries

### Key Features

✅ **No external ML libraries** (sklearn, TensorFlow, etc.)  
✅ **Fast execution** (<100ms per recommendation set)  
✅ **Caching support** (Django cache framework)  
✅ **REST API** (JSON responses)  
✅ **Well documented** with examples  

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend                         │
│  - JavaScript API calls                             │
│  - Recommendation carousels                         │
│  - Play tracking                                    │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              REST API (Views)                       │
│  - recommendation_views.py                          │
│  - JSON responses                                   │
│  - Authentication                                   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│          Recommendation Engine                      │
│  - recommendations.py                               │
│  - Content-based filtering                          │
│  - Collaborative filtering                          │
│  - TF-IDF similarity                                │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│               Data Layer                            │
│  - ListeningHistory model                           │
│  - MusicFile model                                  │
│  - User model                                       │
│  - Django ORM queries                               │
└─────────────────────────────────────────────────────┘
```

---

## 🧠 Algorithms

### 1. Similar Tracks (Content-Based)

**How it works:**

```python
score = (genre_match * 0.5) + (artist_match * 0.3) + (title_similarity * 0.2)
```

- **Genre match:** 50% weight (same genre = 0.5 score)
- **Artist match:** 30% weight (same artist = 0.3 score)
- **Title similarity:** 20% weight (Jaccard coefficient)

**Example:**

```python
from music.recommendations import get_similar_tracks

track = MusicFile.objects.get(id=track_id)
similar = get_similar_tracks(track, limit=10)
```

### 2. Personalized Recommendations (Hybrid)

**Algorithm steps:**

1. Analyze user's listening history (last 30 days)
2. Extract top 3 favorite genres
3. Extract top 5 favorite artists
4. Build recommendation pool:
   - 50% from favorite genres
   - 30% from favorite artists
   - 20% exploration (new popular tracks)
5. Exclude already listened tracks
6. Order by popularity

**Example:**

```python
from music.recommendations import get_recommendations_for_user

recommendations = get_recommendations_for_user(request.user, limit=20)
```

### 3. Top Charts (Popularity-Based)

**How it works:**

- Count plays in time period (7/30 days)
- Order by play count descending
- Use `ListeningHistory` aggregation

**Example:**

```python
from music.recommendations import get_top_charts

# Weekly charts
weekly = get_top_charts(period_days=7, limit=20)

# Monthly charts
monthly = get_top_charts(period_days=30, limit=20)
```

### 4. Continue Listening (User History)

**Algorithm:**

1. Find incomplete plays (completion < 80%)
2. Get tracks from recently listened albums
3. Order by recency
4. Limit results

**Example:**

```python
from music.recommendations import get_continue_listening

continue_tracks = get_continue_listening(request.user, limit=10)
```

### 5. TF-IDF + Cosine Similarity

**Pure Python implementation:**

```python
from music.recommendations import TFIDFSimilarity

# Initialize
tfidf = TFIDFSimilarity()

# Fit on documents (track titles)
documents = [track.title for track in tracks]
tfidf.fit(documents)

# Transform and compare
vec1 = tfidf.transform(track1.title)
vec2 = tfidf.transform(track2.title)
similarity = tfidf.cosine_similarity(vec1, vec2)
```

---

## 🔌 API Reference

### Base URL

```
http://localhost:8000/music/api/
```

### Endpoints

#### 1. Personalized Recommendations

```http
GET /api/recommendations/
```

**Auth:** Required  
**Query params:**
- `limit` (int, default=20, max=50)

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
      "cover_url": "/media/covers/...",
      "play_count": 42
    }
  ],
  "count": 20,
  "user": "username"
}
```

#### 2. Similar Tracks

```http
GET /api/track/<track_id>/similar/
```

**Auth:** Not required  
**Query params:**
- `limit` (int, default=10, max=30)

#### 3. Top Charts

```http
GET /api/charts/
```

**Auth:** Not required  
**Query params:**
- `period` ('weekly' or 'monthly', default='weekly')
- `limit` (int, default=20, max=50)

#### 4. Continue Listening

```http
GET /api/continue-listening/
```

**Auth:** Required  
**Query params:**
- `limit` (int, default=10, max=20)

#### 5. Record Play

```http
POST /api/track/<track_id>/play/
```

**Auth:** Required  
**Body (JSON):**

```json
{
  "duration": 180,
  "position": 180,
  "source": "recommendations",
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

#### 6. Listening Stats

```http
GET /api/listening-stats/
```

**Auth:** Required  
**Query params:**
- `days` (int, default=30, max=365)

**Response:**

```json
{
  "status": "success",
  "stats": {
    "total_plays": 150,
    "unique_tracks": 75,
    "total_duration": 27000,
    "skip_rate": 0.15,
    "completion_rate": 0.85
  },
  "period_days": 30
}
```

---

## 🎨 Frontend Integration

### JavaScript Setup

```html
<!-- Include CSS -->
<link rel="stylesheet" href="{% static 'music/css/recommendations.css' %}">

<!-- Include JS -->
<script src="{% static 'music/js/recommendations.js' %}" defer></script>
```

### HTML Containers

```html
<!-- Personalized Recommendations -->
<section class="recommendation-section">
    <h2><i class="fas fa-magic"></i> Recommended for You</h2>
    <div id="personalized-recommendations"></div>
</section>

<!-- Top Charts -->
<section class="recommendation-section">
    <h2><i class="fas fa-fire"></i> Top Charts</h2>
    <div id="top-charts"></div>
</section>

<!-- Continue Listening -->
<section class="recommendation-section">
    <h2><i class="fas fa-history"></i> Continue Listening</h2>
    <div id="continue-listening"></div>
</section>
```

### JavaScript API

```javascript
// Load personalized recommendations
Recommendations.loadPersonalizedRecommendations(20);

// Load similar tracks
Recommendations.loadSimilarTracks('track-uuid', 10);

// Load charts
Recommendations.loadTopCharts('weekly', 20);

// Record play
Recommendations.recordPlay('track-uuid', 180, 180, 'web');
```

---

## 💾 Data Models

### ListeningHistory

```python
class ListeningHistory(models.Model):
    user = ForeignKey(User)
    track = ForeignKey(MusicFile)
    played_at = DateTimeField()
    playback_duration = IntegerField()  # seconds
    completion_percentage = IntegerField()  # 0-100
    playback_position = IntegerField()  # seconds
    source = CharField()  # 'playlist', 'album', 'search', etc.
    device = CharField()  # 'web', 'mobile', 'desktop'
    skipped = BooleanField()  # True if <30% completed
    repeated = BooleanField()  # True if replayed within 1 hour
```

### Recording a Play

```python
from music.models import ListeningHistory

ListeningHistory.record_play(
    user=request.user,
    track=track,
    duration=180,  # How long listened
    position=180,  # Where stopped
    source='recommendations',
    device='web'
)
```

---

## ⚡ Performance

### Optimization Tips

1. **Enable caching:**

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Database indexes:**

```python
# Already included in models.py
class Meta:
    indexes = [
        models.Index(fields=['user', '-played_at']),
        models.Index(fields=['track', '-played_at']),
    ]
```

3. **Prefetch related:**

```python
tracks = MusicFile.objects.select_related(
    'artist', 'album', 'genre'
).prefetch_related(
    'play_history'
)
```

### Benchmarks

| Operation | Average Time | Cache Hit |
|-----------|--------------|----------|
| Personalized (20) | 45ms | 2ms |
| Similar Tracks (10) | 35ms | 1ms |
| Top Charts (20) | 25ms | 1ms |
| Continue Listening (10) | 30ms | 2ms |

---

## 📚 Examples

### Example 1: Add Recommendations to Homepage

```python
# views.py
from music.recommendations import get_recommendations_for_user, get_top_charts

def index(request):
    context = {}
    
    if request.user.is_authenticated:
        context['recommendations'] = get_recommendations_for_user(
            request.user, 
            limit=20
        )
    
    context['charts'] = get_top_charts(period_days=7, limit=20)
    
    return render(request, 'music/index.html', context)
```

### Example 2: Track Play Events

```javascript
// In your audio player
audio.addEventListener('ended', () => {
    const duration = Math.floor(audio.currentTime);
    
    Recommendations.recordPlay(
        currentTrack.id,
        duration,
        duration,
        'player'
    );
});
```

### Example 3: Custom Recommendation Algorithm

```python
from music.recommendations import RecommendationEngine

engine = RecommendationEngine(cache_timeout=3600)

# Get recommendations with custom settings
recommendations = engine.get_personalized_recommendations(
    user=request.user,
    limit=50,
    use_cache=False  # Force fresh results
)
```

---

## 🔧 Configuration

### Engine Settings

```python
# music/recommendations.py
class RecommendationEngine:
    def __init__(self, cache_timeout=3600):
        self.cache_timeout = cache_timeout  # 1 hour default
```

### JavaScript Settings

```javascript
// music/static/music/js/recommendations.js
Recommendations.config = {
    apiBaseUrl: '/music/api',
    refreshInterval: 60000,  // 1 minute
    cacheTimeout: 300000,    // 5 minutes
    defaultLimit: 20,
};
```

---

## 🚀 Next Steps

### Planned Improvements (v2.0)

- [ ] Matrix factorization (collaborative filtering)
- [ ] Deep learning embeddings (optional)
- [ ] Real-time streaming recommendations
- [ ] A/B testing framework
- [ ] Explainable AI (why was this recommended?)
- [ ] Multi-language support

---

## 🤝 Contributing

Want to improve the recommendation engine? Check out:

1. **Algorithm improvements** - Better similarity metrics
2. **Performance** - Faster queries, better caching
3. **Features** - New recommendation types
4. **Documentation** - More examples, tutorials

---

## 📄 License

MIT License - Part of Music Stream App

---

**Made with ❤️ by vitorpixel-6436**

*Powered by Django, Python, and pure mathematics* 🧮
