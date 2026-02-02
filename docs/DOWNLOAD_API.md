# Download Manager API Documentation

## Overview

Comprehensive API for managing download tasks from YouTube, SoundCloud, Bandcamp, and direct URLs.

---

## Endpoints

### 1. Create Download Task

**POST** `/music/downloads/create/`

Create a new download task.

#### Request Body (Form Data)

```json
{
  "url": "https://youtube.com/watch?v=...",
  "output_format": "mp3",
  "output_quality": "320k"
}
```

#### Response

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Download task created successfully",
  "redirect_url": "/music/downloads/"
}
```

---

### 2. Get Task Status

**GET** `/music/api/downloads/<task_id>/status/`

Get real-time status of a download task.

#### Response

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "downloading",
  "progress": 45,
  "current_step": "Extracting audio...",
  "is_active": true,
  "elapsed_seconds": 12.5,
  "error_message": null,
  "result": null
}
```

#### Status Values

- `pending` - Task created, waiting to start
- `downloading` - Currently downloading
- `processing` - Converting/processing audio
- `completed` - Successfully completed
- `failed` - Failed with error
- `cancelled` - Cancelled by user

#### Completed Task Response

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "is_active": false,
  "result": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "Amazing Song",
    "artist": "Artist Name",
    "url": "/music/player/660e8400-e29b-41d4-a716-446655440001/"
  }
}
```

---

### 3. List Download Tasks

**GET** `/music/downloads/`

List all download tasks with filtering and pagination.

#### Query Parameters

- `status` - Filter by status (`all`, `pending`, `downloading`, `completed`, `failed`)
- `source` - Filter by source (`all`, `youtube`, `soundcloud`, `bandcamp`, `url`)
- `q` - Search query (searches URL, title, artist)
- `sort` - Sort order (`-created_at`, `created_at`, `-completed_at`, `status`)
- `page` - Page number (default: 1)

#### Example

```
GET /music/downloads/?status=completed&source=youtube&page=1
```

---

### 4. Cancel Download Task

**POST** `/music/downloads/<task_id>/cancel/`

Cancel an active download task.

#### Response

```json
{
  "success": true,
  "message": "Task cancelled successfully"
}
```

#### Error Response

```json
{
  "success": false,
  "error": "Task is not active"
}
```

---

### 5. Retry Failed Task

**POST** `/music/downloads/<task_id>/retry/`

Retry a failed download task (creates new task with same parameters).

#### Response

```json
{
  "success": true,
  "new_task_id": "770e8400-e29b-41d4-a716-446655440002",
  "message": "Task retry successful"
}
```

---

### 6. Bulk Status Check

**GET** `/music/api/downloads/bulk-status/?task_ids=uuid1,uuid2,uuid3`

Get status of multiple tasks in one request (max 50 tasks).

#### Query Parameters

- `task_ids` - Comma-separated list of task UUIDs

#### Response

```json
{
  "success": true,
  "count": 3,
  "tasks": [
    {
      "task_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "downloading",
      "progress": 45,
      "current_step": "Downloading...",
      "is_active": true
    },
    {
      "task_id": "660e8400-e29b-41d4-a716-446655440001",
      "status": "completed",
      "progress": 100,
      "is_active": false,
      "result": {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "title": "Song Title",
        "artist": "Artist Name"
      }
    }
  ]
}
```

---

## Frontend Integration

### Polling for Progress Updates

```javascript
function pollTaskStatus(taskId) {
  const interval = setInterval(async () => {
    try {
      const response = await fetch(`/music/api/downloads/${taskId}/status/`);
      const data = await response.json();
      
      // Update UI
      updateProgressBar(data.progress);
      updateStatus(data.current_step);
      
      // Stop polling when complete
      if (!data.is_active) {
        clearInterval(interval);
        
        if (data.status === 'completed') {
          showSuccess(data.result);
        } else if (data.status === 'failed') {
          showError(data.error_message);
        }
      }
    } catch (error) {
      console.error('Polling error:', error);
      clearInterval(interval);
    }
  }, 2000); // Poll every 2 seconds
}
```

### Creating a Download Task (AJAX)

```javascript
async function createDownloadTask(url, format, quality) {
  const formData = new FormData();
  formData.append('url', url);
  formData.append('output_format', format);
  formData.append('output_quality', quality);
  
  const response = await fetch('/music/downloads/create/', {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCsrfToken()
    },
    body: formData
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Start polling for progress
    pollTaskStatus(data.task_id);
  } else {
    console.error('Error:', data.error);
  }
}
```

### Cancelling a Task

```javascript
async function cancelTask(taskId) {
  const response = await fetch(`/music/downloads/${taskId}/cancel/`, {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCsrfToken()
    }
  });
  
  const data = await response.json();
  
  if (data.success) {
    console.log('Task cancelled');
  }
}
```

---

## Error Handling

### Common Error Codes

- `400` - Bad request (invalid parameters)
- `404` - Task not found or access denied
- `500` - Internal server error

### Error Response Format

```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## Rate Limiting

- Maximum 50 active downloads per user
- Bulk status API limited to 50 tasks per request
- Status polling recommended every 2-3 seconds

---

## Security

- All endpoints require authentication (`@login_required`)
- CSRF protection enabled for all POST requests
- Users can only access their own download tasks
- URL validation prevents malicious inputs

---

## Next Steps

See [DOWNLOAD_IMPLEMENTATION.md](DOWNLOAD_IMPLEMENTATION.md) for backend implementation details.
