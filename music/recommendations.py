"""
Recommendation Engine for Music Stream App
============================================

ML-powered music recommendations using:
- Content-based filtering (genre, artist, text similarity)
- Simplified collaborative filtering (user behavior patterns)
- TF-IDF + Cosine Similarity (without sklearn)
- Fast execution (<100ms)

No external ML dependencies - pure Python + Django ORM.
"""

import math
import logging
from collections import Counter, defaultdict
from datetime import timedelta
from django.db.models import Count, Q, F
from django.utils import timezone
from django.core.cache import cache

logger = logging.getLogger(__name__)


# ============================================================================
# CORE RECOMMENDATION ENGINE
# ============================================================================

class RecommendationEngine:
    """
    Main recommendation engine with multiple algorithms.
    
    Algorithms:
    1. Similar tracks (content-based)
    2. Personalized recommendations (hybrid)
    3. Top charts (popularity-based)
    4. Continue listening (user history)
    """
    
    def __init__(self, cache_timeout=3600):
        """
        Initialize recommendation engine.
        
        Args:
            cache_timeout: Cache timeout in seconds (default 1 hour)
        """
        self.cache_timeout = cache_timeout
    
    # ========================================================================
    # 1. SIMILAR TRACKS (Content-Based)
    # ========================================================================
    
    def get_similar_tracks(self, track, limit=10, use_cache=True):
        """
        Find tracks similar to given track using content-based filtering.
        
        Similarity factors:
        - Same genre (50% weight)
        - Same artist (30% weight)
        - Text similarity in title (20% weight)
        
        Args:
            track: MusicFile instance
            limit: Number of recommendations
            use_cache: Use cached results
        
        Returns:
            QuerySet of similar MusicFile objects
        """
        from music.models import MusicFile
        
        cache_key = f"similar_tracks_{track.id}_{limit}"
        
        if use_cache:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        # Score-based filtering
        similar_tracks = []
        
        # Get all candidates (exclude current track)
        candidates = MusicFile.objects.exclude(id=track.id).select_related(
            'artist', 'genre', 'album'
        )
        
        for candidate in candidates:
            score = 0.0
            
            # Genre match (50%)
            if track.genre and candidate.genre == track.genre:
                score += 0.5
            
            # Artist match (30%)
            if track.artist == candidate.artist:
                score += 0.3
            
            # Title similarity (20%)
            title_sim = self._text_similarity(track.title, candidate.title)
            score += 0.2 * title_sim
            
            similar_tracks.append((candidate, score))
        
        # Sort by score descending
        similar_tracks.sort(key=lambda x: x[1], reverse=True)
        
        # Get top results
        result_ids = [t[0].id for t in similar_tracks[:limit]]
        result = MusicFile.objects.filter(id__in=result_ids)
        
        if use_cache:
            cache.set(cache_key, result, self.cache_timeout)
        
        return result
    
    # ========================================================================
    # 2. PERSONALIZED RECOMMENDATIONS (Hybrid)
    # ========================================================================
    
    def get_personalized_recommendations(self, user, limit=20, use_cache=True):
        """
        Get personalized recommendations for user.
        
        Algorithm:
        1. Analyze user's listening history
        2. Find favorite genres, artists
        3. Mix popular tracks from favorite categories
        4. Add some exploration (new artists)
        
        Args:
            user: User instance
            limit: Number of recommendations
            use_cache: Use cached results
        
        Returns:
            List of MusicFile instances
        """
        from music.models import MusicFile, ListeningHistory
        
        cache_key = f"personalized_recs_{user.id}_{limit}"
        
        if use_cache:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        # Get user's listening history (last 30 days)
        recent_cutoff = timezone.now() - timedelta(days=30)
        user_history = ListeningHistory.objects.filter(
            user=user,
            played_at__gte=recent_cutoff
        ).select_related('track__artist', 'track__genre')
        
        if not user_history.exists():
            # No history - return popular tracks
            return self.get_top_charts(limit=limit, period_days=7)
        
        # Analyze user preferences
        favorite_genres = self._get_top_genres_from_history(user_history, top_n=3)
        favorite_artists = self._get_top_artists_from_history(user_history, top_n=5)
        
        # Get already listened track IDs (exclude from recommendations)
        listened_ids = user_history.values_list('track_id', flat=True)
        
        # Build recommendation pool
        recommendations = []
        
        # 1. Tracks from favorite genres (50%)
        genre_tracks = MusicFile.objects.filter(
            genre__in=favorite_genres
        ).exclude(
            id__in=listened_ids
        ).order_by('-play_count')[:int(limit * 0.5)]
        
        recommendations.extend(genre_tracks)
        
        # 2. Tracks from favorite artists (30%)
        artist_tracks = MusicFile.objects.filter(
            artist__in=favorite_artists
        ).exclude(
            id__in=listened_ids
        ).exclude(
            id__in=[t.id for t in recommendations]
        ).order_by('-play_count')[:int(limit * 0.3)]
        
        recommendations.extend(artist_tracks)
        
        # 3. Exploration - popular new tracks (20%)
        exploration_tracks = MusicFile.objects.exclude(
            id__in=listened_ids
        ).exclude(
            id__in=[t.id for t in recommendations]
        ).order_by('-created_at', '-play_count')[:int(limit * 0.2)]
        
        recommendations.extend(exploration_tracks)
        
        # Limit final result
        result = recommendations[:limit]
        
        if use_cache:
            cache.set(cache_key, result, self.cache_timeout)
        
        return result
    
    # ========================================================================
    # 3. TOP CHARTS (Popularity-Based)
    # ========================================================================
    
    def get_top_charts(self, limit=20, period_days=7, use_cache=True):
        """
        Get top trending tracks based on play count.
        
        Args:
            limit: Number of tracks
            period_days: Time period (7 = weekly, 30 = monthly)
            use_cache: Use cached results
        
        Returns:
            QuerySet of MusicFile objects
        """
        from music.models import MusicFile, ListeningHistory
        
        cache_key = f"top_charts_{period_days}_{limit}"
        
        if use_cache:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        cutoff_date = timezone.now() - timedelta(days=period_days)
        
        # Count plays in period
        top_tracks = ListeningHistory.objects.filter(
            played_at__gte=cutoff_date
        ).values('track').annotate(
            plays=Count('id')
        ).order_by('-plays')[:limit]
        
        track_ids = [item['track'] for item in top_tracks]
        
        # Get full track objects in correct order
        result = MusicFile.objects.filter(id__in=track_ids).select_related(
            'artist', 'genre', 'album'
        )
        
        # Preserve order from annotation
        result = sorted(result, key=lambda t: track_ids.index(t.id))
        
        if use_cache:
            cache.set(cache_key, result, self.cache_timeout)
        
        return result
    
    # ========================================================================
    # 4. CONTINUE LISTENING (User History)
    # ========================================================================
    
    def get_continue_listening(self, user, limit=10, use_cache=True):
        """
        Get tracks to continue listening based on recent incomplete plays.
        
        Algorithm:
        - Recent tracks that user didn't finish
        - Tracks from recently listened albums
        - Next tracks in playlists
        
        Args:
            user: User instance
            limit: Number of recommendations
            use_cache: Use cached results
        
        Returns:
            List of MusicFile instances
        """
        from music.models import MusicFile, ListeningHistory
        
        cache_key = f"continue_listening_{user.id}_{limit}"
        
        if use_cache:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        # Get recent listening history (last 7 days)
        recent_cutoff = timezone.now() - timedelta(days=7)
        recent_history = ListeningHistory.objects.filter(
            user=user,
            played_at__gte=recent_cutoff
        ).select_related('track__artist', 'track__album').order_by('-played_at')[:50]
        
        if not recent_history.exists():
            return []
        
        recommendations = []
        seen_track_ids = set()
        
        # 1. Incomplete plays (didn't finish track)
        for entry in recent_history:
            if entry.completion_percentage and entry.completion_percentage < 80:
                if entry.track.id not in seen_track_ids:
                    recommendations.append(entry.track)
                    seen_track_ids.add(entry.track.id)
        
        # 2. Tracks from recently listened albums
        recent_albums = [entry.track.album for entry in recent_history if entry.track.album]
        recent_albums = list(set(recent_albums))[:3]  # Top 3 recent albums
        
        for album in recent_albums:
            album_tracks = MusicFile.objects.filter(
                album=album
            ).exclude(id__in=seen_track_ids).order_by('title')[:2]
            
            for track in album_tracks:
                recommendations.append(track)
                seen_track_ids.add(track.id)
        
        # Limit result
        result = recommendations[:limit]
        
        if use_cache:
            cache.set(cache_key, result, self.cache_timeout)
        
        return result
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _text_similarity(self, text1, text2):
        """
        Calculate text similarity using Jaccard coefficient.
        
        Simple but effective for short texts like song titles.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0.0 - 1.0)
        """
        # Normalize and tokenize
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Jaccard coefficient
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _get_top_genres_from_history(self, history_queryset, top_n=3):
        """
        Extract top N genres from listening history.
        
        Args:
            history_queryset: ListeningHistory QuerySet
            top_n: Number of top genres
        
        Returns:
            List of Genre instances
        """
        genre_counts = Counter()
        
        for entry in history_queryset:
            if entry.track.genre:
                genre_counts[entry.track.genre] += 1
        
        # Get top N
        top_genres = [genre for genre, count in genre_counts.most_common(top_n)]
        return top_genres
    
    def _get_top_artists_from_history(self, history_queryset, top_n=5):
        """
        Extract top N artists from listening history.
        
        Args:
            history_queryset: ListeningHistory QuerySet
            top_n: Number of top artists
        
        Returns:
            List of Artist instances
        """
        artist_counts = Counter()
        
        for entry in history_queryset:
            if entry.track.artist:
                artist_counts[entry.track.artist] += 1
        
        # Get top N
        top_artists = [artist for artist, count in artist_counts.most_common(top_n)]
        return top_artists


# ============================================================================
# TF-IDF + COSINE SIMILARITY (Pure Python)
# ============================================================================

class TFIDFSimilarity:
    """
    TF-IDF and Cosine Similarity implementation without sklearn.
    
    Used for advanced text-based track similarity.
    """
    
    def __init__(self):
        self.documents = []
        self.vocab = set()
        self.idf_scores = {}
    
    def fit(self, documents):
        """
        Fit TF-IDF model on documents.
        
        Args:
            documents: List of text strings
        """
        self.documents = documents
        
        # Build vocabulary
        for doc in documents:
            words = set(doc.lower().split())
            self.vocab.update(words)
        
        # Calculate IDF scores
        num_docs = len(documents)
        
        for word in self.vocab:
            # Count documents containing word
            doc_count = sum(1 for doc in documents if word in doc.lower())
            
            # IDF formula: log(N / df)
            self.idf_scores[word] = math.log(num_docs / (doc_count + 1))
    
    def transform(self, document):
        """
        Transform document to TF-IDF vector.
        
        Args:
            document: Text string
        
        Returns:
            Dict of {word: tfidf_score}
        """
        words = document.lower().split()
        word_counts = Counter(words)
        
        # Calculate TF-IDF
        tfidf_vector = {}
        
        for word, count in word_counts.items():
            if word in self.vocab:
                # TF: term frequency
                tf = count / len(words)
                
                # TF-IDF
                tfidf_vector[word] = tf * self.idf_scores.get(word, 0)
        
        return tfidf_vector
    
    def cosine_similarity(self, vec1, vec2):
        """
        Calculate cosine similarity between two TF-IDF vectors.
        
        Args:
            vec1: First TF-IDF vector (dict)
            vec2: Second TF-IDF vector (dict)
        
        Returns:
            Similarity score (0.0 - 1.0)
        """
        # Get common words
        common_words = set(vec1.keys()).intersection(set(vec2.keys()))
        
        if not common_words:
            return 0.0
        
        # Dot product
        dot_product = sum(vec1[word] * vec2[word] for word in common_words)
        
        # Magnitudes
        magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_similar_tracks(track, limit=10):
    """
    Convenience function for getting similar tracks.
    
    Args:
        track: MusicFile instance
        limit: Number of results
    
    Returns:
        QuerySet of similar tracks
    """
    engine = RecommendationEngine()
    return engine.get_similar_tracks(track, limit=limit)


def get_recommendations_for_user(user, limit=20):
    """
    Convenience function for personalized recommendations.
    
    Args:
        user: User instance
        limit: Number of results
    
    Returns:
        List of recommended tracks
    """
    engine = RecommendationEngine()
    return engine.get_personalized_recommendations(user, limit=limit)


def get_top_charts(period_days=7, limit=20):
    """
    Convenience function for top charts.
    
    Args:
        period_days: Period (7=weekly, 30=monthly)
        limit: Number of results
    
    Returns:
        QuerySet of top tracks
    """
    engine = RecommendationEngine()
    return engine.get_top_charts(period_days=period_days, limit=limit)


def get_continue_listening(user, limit=10):
    """
    Convenience function for continue listening.
    
    Args:
        user: User instance
        limit: Number of results
    
    Returns:
        List of tracks to continue
    """
    engine = RecommendationEngine()
    return engine.get_continue_listening(user, limit=limit)
