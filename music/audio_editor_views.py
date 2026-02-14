"""Audio Editor REST API Views.

Provides endpoints for managing audio editing projects:
- Project CRUD operations
- Preview/export rendering
- Track management within projects
"""

import logging
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from .models_editor import AudioEditProject
from .audio_editor import AudioEditorEngine

logger = logging.getLogger(__name__)


class AudioEditProjectSerializer:
    """Serializer for AudioEditProject (without DRF to keep it simple)."""
    
    @staticmethod
    def to_dict(project):
        return {
            'id': str(project.id),
            'name': project.name,
            'description': project.description,
            'base_track': {
                'id': str(project.base_track.id),
                'title': project.base_track.title,
                'artist': project.base_track.artist,
                'duration': project.base_track.duration,
            },
            'result_track': str(project.result_track.id) if project.result_track else None,
            'config': project.get_config(),
            'layer_count': len(project.get_layers()),
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat(),
        }


class AudioEditProjectViewSet(viewsets.ViewSet):
    """ViewSet for audio editing projects."""
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List all projects for current user."""
        projects = AudioEditProject.objects.filter(
            user=request.user
        ).order_by('-updated_at')
        
        data = [AudioEditProjectSerializer.to_dict(p) for p in projects]
        return Response(data)
    
    def create(self, request):
        """Create new editing project."""
        try:
            name = request.data.get('name', 'Untitled Mix')
            description = request.data.get('description', '')
            base_track_id = request.data.get('base_track_id')
            
            if not base_track_id:
                return Response(
                    {'error': 'base_track_id required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            from .models import MusicFile
            try:
                base_track = MusicFile.objects.get(id=base_track_id)
            except MusicFile.DoesNotExist:
                return Response(
                    {'error': 'Base track not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            project = AudioEditProject.objects.create(
                user=request.user,
                name=name,
                description=description,
                base_track=base_track
            )
            
            logger.info(f'Created audio project {project.id} for user {request.user.username}')
            return Response(
                AudioEditProjectSerializer.to_dict(project),
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            logger.error(f'Failed to create project: {e}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Get project details."""
        try:
            project = AudioEditProject.objects.get(
                id=pk,
                user=request.user
            )
            return Response(AudioEditProjectSerializer.to_dict(project))
        except AudioEditProject.DoesNotExist:
            return Response(
                {'error': 'Project not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, pk=None):
        """Update project config."""
        try:
            project = get_object_or_404(
                AudioEditProject,
                id=pk,
                user=request.user
            )
            
            # Update basic fields
            if 'name' in request.data:
                project.name = request.data['name']
            if 'description' in request.data:
                project.description = request.data['description']
            
            # Update config
            if 'config' in request.data:
                project.config = request.data['config']
            
            project.save()
            logger.info(f'Updated project {project.id}')
            
            return Response(AudioEditProjectSerializer.to_dict(project))
        
        except Exception as e:
            logger.error(f'Failed to update project: {e}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, pk=None):
        """Delete project."""
        try:
            project = get_object_or_404(
                AudioEditProject,
                id=pk,
                user=request.user
            )
            project.delete()
            logger.info(f'Deleted project {pk}')
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            logger.error(f'Failed to delete project: {e}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], url_path='preview')
    def preview(self, request, pk=None):
        """Generate preview for project."""
        try:
            project = get_object_or_404(
                AudioEditProject,
                id=pk,
                user=request.user
            )
            
            # Update config if provided
            if 'config' in request.data:
                project.config = request.data['config']
                project.save(update_fields=['config'])
            
            # Render preview
            engine = AudioEditorEngine(project)
            preview_path = engine.render_preview('mp3')
            
            logger.info(f'Generated preview for project {project.id}')
            
            return Response({
                'status': 'preview_ready',
                'preview_url': f'/media/editor/temp/{project.id}_preview.mp3'
            })
        
        except Exception as e:
            logger.error(f'Preview generation failed: {e}')
            return Response(
                {'error': f'Preview failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], url_path='export')
    def export_final(self, request, pk=None):
        """Export project as final MusicFile."""
        try:
            project = get_object_or_404(
                AudioEditProject,
                id=pk,
                user=request.user
            )
            
            # Get export options
            export_format = request.data.get('format', 'flac')
            export_bitrate = request.data.get('bitrate', '320k')
            
            # Render final
            engine = AudioEditorEngine(project)
            music_file = engine.render_final(export_format, export_bitrate)
            
            logger.info(f'Exported project {project.id} as MusicFile {music_file.id}')
            
            from .models import MusicFile
            from .serializers import MusicFileSerializer  # existing serializer
            
            # Return created MusicFile
            return Response({
                'status': 'exported',
                'music_file': {
                    'id': str(music_file.id),
                    'title': music_file.title,
                    'artist': music_file.artist,
                    'duration': music_file.duration,
                    'url': music_file.file.url if music_file.file else None,
                }
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f'Export failed: {e}')
            return Response(
                {'error': f'Export failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], url_path='add-layer')
    def add_layer(self, request, pk=None):
        """Add new mixing layer to project."""
        try:
            project = get_object_or_404(
                AudioEditProject,
                id=pk,
                user=request.user
            )
            
            track_id = request.data.get('track_id')
            offset_ms = request.data.get('offset_ms', 0)
            gain_db = request.data.get('gain_db', 0.0)
            fade_in_ms = request.data.get('fade_in_ms', 0)
            fade_out_ms = request.data.get('fade_out_ms', 0)
            
            if not track_id:
                return Response(
                    {'error': 'track_id required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify track exists
            from .models import MusicFile
            try:
                MusicFile.objects.get(id=track_id)
            except MusicFile.DoesNotExist:
                return Response(
                    {'error': 'Track not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Add layer
            project.add_layer(
                track_id=track_id,
                offset_ms=int(offset_ms),
                gain_db=float(gain_db),
                fade_in_ms=int(fade_in_ms),
                fade_out_ms=int(fade_out_ms)
            )
            project.save()
            
            logger.info(f'Added layer {track_id} to project {project.id}')
            return Response(AudioEditProjectSerializer.to_dict(project))
        
        except Exception as e:
            logger.error(f'Failed to add layer: {e}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
