from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime
import os
import shutil
from pathlib import Path
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/videos", tags=["videos"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/videos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class UploadVideoRequest(BaseModel):
    title: str
    description: str
    url: str
    duration_seconds: int
    topic_id: int
    has_subtitles: bool = False
    resolution_options: dict = None

@router.get("/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video details with all content"""
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    concepts = db.query(models.VideoConcept).filter(models.VideoConcept.video_id == video_id).all()
    subtitles = db.query(models.Subtitle).filter(models.Subtitle.video_id == video_id).all()

    return {
        "video": {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "url": video.url if video.url.startswith('http') else f"/api/v1/videos/file/{video.url}",
            "duration_seconds": video.duration_seconds,
            "topic": video.topic,
            "has_subtitles": video.has_subtitles,
            "resolution_options": video.resolution_options
        },
        "concepts": [{
            "id": c.id,
            "title": c.title,
            "content": c.content,
            "explanation": c.explanation,
            "real_world_example": c.real_world_example
        } for c in concepts],
        "subtitles": [{
            "language": s.language,
            "content": s.content
        } for s in subtitles]
    }

@router.post("/{video_id}/track-watch")
def track_video_watch(
    video_id: int,
    student_id: int,
    duration_seconds: int,
    completion_percentage: int,
    db: Session = Depends(get_db)
):
    """Track video watch history"""
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Check if watch history exists
    watch = db.query(models.VideoWatchHistory).filter(
        models.VideoWatchHistory.student_id == student_id,
        models.VideoWatchHistory.video_id == video_id
    ).first()

    if watch:
        watch.watch_duration_seconds = duration_seconds
        watch.completion_percentage = completion_percentage
        watch.watch_end_time = datetime.utcnow()
        if completion_percentage >= 80:
            watch.is_completed = True
    else:
        watch = models.VideoWatchHistory(
            student_id=student_id,
            video_id=video_id,
            watch_duration_seconds=duration_seconds,
            completion_percentage=completion_percentage,
            is_completed=completion_percentage >= 80
        )
        db.add(watch)

    db.commit()

    return {
        "status": "tracked",
        "is_completed": watch.is_completed,
        "completion_percentage": watch.completion_percentage
    }

@router.get("/lesson/{lesson_id}/videos")
def get_lesson_videos(lesson_id: int, db: Session = Depends(get_db)):
    """Get all videos for a lesson"""
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    videos = db.query(models.Video).filter(models.Video.lesson_id == lesson_id).all()

    return {
        "lesson": {
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description
        },
        "videos": [{
            "id": v.id,
            "title": v.title,
            "duration_seconds": v.duration_seconds,
            "has_subtitles": v.has_subtitles
        } for v in videos]
    }

@router.get("/file/{filename}")
def get_video_file(filename: str):
    """Serve uploaded video files"""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )

@router.get("/topic/{topic}")
def get_videos_by_topic(topic: str, db: Session = Depends(get_db)):
    """Get all videos for a specific topic"""
    valid_topics = ['lm', 'nlp', 'da']
    if topic not in valid_topics:
        raise HTTPException(status_code=400, detail="Invalid topic. Must be one of: lm, nlp, da")

    videos = db.query(models.Video).filter(models.Video.topic == topic).all()

    return {
        "topic": topic,
        "videos": [{
            "id": v.id,
            "title": v.title,
            "description": v.description,
            "url": v.url if v.url.startswith('http') else f"/api/v1/videos/file/{v.url}",
            "duration_seconds": v.duration_seconds,
            "topic": v.topic,
            "has_subtitles": v.has_subtitles,
            "created_at": v.created_at.isoformat() if v.created_at else None
        } for v in videos]
    }
def get_video_concepts(video_id: int, db: Session = Depends(get_db)):
    """Get concepts explained in a video"""
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    concepts = db.query(models.VideoConcept).filter(models.VideoConcept.video_id == video_id).all()

    return {
        "video_title": video.title,
        "concepts": [{
            "id": c.id,
            "title": c.title,
            "content": c.content,
            "explanation": c.explanation,
            "real_world_example": c.real_world_example
        } for c in concepts]
    }

@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    duration_seconds: int = Form(...),
    topic: str = Form(...),
    has_subtitles: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Upload a new video file for a topic"""
    # Validate topic
    valid_topics = ['lm', 'nlp', 'da']
    if topic not in valid_topics:
        raise HTTPException(status_code=400, detail="Invalid topic. Must be one of: lm, nlp, da")

    # Validate file type
    allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/flv', 'video/webm']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")

    # Validate file size (max 500MB)
    max_size = 500 * 1024 * 1024  # 500MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 500MB.")

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{title.replace(' ', '_')}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create video record in database
    video = models.Video(
        title=title,
        description=description,
        url=str(file_path),  # Store file path as URL
        duration_seconds=duration_seconds,
        lesson_id=1,  # Default lesson_id for now
        topic=topic,  # Store the topic category
        has_subtitles=has_subtitles,
        resolution_options={}
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return {
        "success": True,
        "video": {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "url": str(file_path),
            "duration_seconds": video.duration_seconds,
            "topic": video.topic,
            "has_subtitles": video.has_subtitles,
            "file_size": len(file_content)
        }
    }
