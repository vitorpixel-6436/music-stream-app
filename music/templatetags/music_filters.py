from django import template

register = template.Library()

@register.filter
def format_duration(seconds):
    """
    Convert seconds to MM:SS format
    """
    if not seconds:
        return '--:--'
    
    try:
        seconds = int(seconds)
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"
    except (ValueError, TypeError):
        return '--:--'
