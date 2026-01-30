from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import MusicFile, Album, Artist, Genre, Playlist

class TrackUploadForm(forms.ModelForm):
    """Form for uploading music tracks"""
    
    class Meta:
        model = MusicFile
        fields = ['title', 'artist', 'album', 'genre', 'file', 'format']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Track title'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'album': forms.Select(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}),
            'format': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_file(self):
        """Validate uploaded file"""
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 50MB as per views.py logic)
            if file.size > 50 * 1024 * 1024:
                raise ValidationError(_('File size must not exceed 50MB'))
            
            # Check file extension
            allowed_extensions = ['mp3', 'wav', 'flac', 'ogg', 'm4a']
            file_ext = file.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                raise ValidationError(_('Unsupported audio format'))
        return file

class PlaylistCreateForm(forms.ModelForm):
    """Form for creating playlists"""
    
    class Meta:
        model = Playlist
        fields = ['name', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Playlist name'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SearchForm(forms.Form):
    """Form for searching tracks"""
    
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tracks...',
            'autocomplete': 'off'
        })
    )
    
    artist = forms.ModelChoiceField(
        queryset=Artist.objects.all(),
        required=False,
        empty_label='All Artists',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort = forms.ChoiceField(
        choices=[
            ('-created_at', 'Newest'),
            ('title', 'A-Z'),
            ('-play_count', 'Popular'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ArtistCreateForm(forms.ModelForm):
    """Form for creating artists"""
    
    class Meta:
        model = Artist
        fields = ['name', 'bio', 'website', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artist name'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Biography'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class AlbumCreateForm(forms.ModelForm):
    """Form for creating albums"""
    
    class Meta:
        model = Album
        fields = ['title', 'artist', 'year', 'genre', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Album title'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'cover': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class URLImportForm(forms.Form):
    """Form for importing music from URLs (YouTube, SoundCloud, etc.)"""
    
    url = forms.URLField(
        max_length=2048,
        required=True,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://youtube.com/watch?v=... or https://soundcloud.com/...',
            'autocomplete': 'off'
        }),
        help_text='Supported: YouTube, SoundCloud, Bandcamp, direct audio URLs'
    )
    
    output_format = forms.ChoiceField(
        choices=MusicFile.FORMAT_CHOICES,
        initial='mp3',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Output audio format'
    )
    
    output_quality = forms.ChoiceField(
        choices=[
            ('320k', '320 kbps (Best)'),
            ('256k', '256 kbps (High)'),
            ('192k', '192 kbps (Medium)'),
            ('128k', '128 kbps (Low)'),
        ],
        initial='320k',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Audio quality/bitrate'
    )
    
    def clean_url(self):
        """Validate and normalize URL"""
        url = self.cleaned_data.get('url')
        if url:
            # Basic validation for supported platforms
            supported_domains = [
                'youtube.com', 'youtu.be',
                'soundcloud.com',
                'bandcamp.com',
            ]
            
            # Allow direct audio file URLs
            audio_extensions = ['.mp3', '.flac', '.wav', '.m4a', '.ogg']
            
            is_supported = any(domain in url.lower() for domain in supported_domains)
            is_direct_audio = any(url.lower().endswith(ext) for ext in audio_extensions)
            
            if not (is_supported or is_direct_audio):
                raise ValidationError(
                    _('URL must be from YouTube, SoundCloud, Bandcamp, or a direct audio file link')
                )
        
        return url
