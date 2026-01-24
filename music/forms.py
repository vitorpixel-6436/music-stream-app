from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import Track, Album, Artist, Genre, Playlist


class TrackUploadForm(forms.ModelForm):
    """Form for uploading music tracks"""
    
    class Meta:
        model = Track
        fields = ['title', 'artist', 'album', 'genre', 'file', 'cover_art', 'format', 'quality']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Track title'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'album': forms.Select(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}),
            'cover_art': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'format': forms.Select(attrs={'class': 'form-control'}),
            'quality': forms.Select(attrs={'class': 'form-control'}),
        }
            
    def clean_file(self):
        """Validate uploaded file"""
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 100MB)
            if file.size > 100 * 1024 * 1024:
                raise ValidationError(_('File size must not exceed 100MB'))
            
            # Check file extension
            allowed_extensions = ['mp3', 'wav', 'flac', 'ogg', 'm4a']
            file_ext = file.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                raise ValidationError(_('Only audio files are allowed'))
        return file


class PlaylistCreateForm(forms.ModelForm):
    """Form for creating playlists"""
    
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Playlist name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SearchForm(forms.Form):
    """Form for searching tracks"""
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for tracks, artists, albums...',
            'autocomplete': 'off'
        })
    )
    
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label='All Genres',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    format = forms.ChoiceField(
        choices=[('', 'All Formats')] + Track.FORMAT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    quality = forms.ChoiceField(
        choices=[('', 'All Qualities')] + Track.QUALITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class DownloadForm(forms.Form):
    """Form for downloading tracks with format conversion"""
    
    target_format = forms.ChoiceField(
        choices=Track.FORMAT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    target_quality = forms.ChoiceField(
        choices=Track.QUALITY_CHOICES,
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
        fields = ['title', 'artist', 'year', 'genre', 'cover_art']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Album title'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'cover_art': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
