from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/api/v1/topics", tags=["topics"])

@router.get("/")
def get_all_topics(db: Session = Depends(get_db)):
    """Get all topics"""
    topics = db.query(models.Topic).all()
    return {
        "topics": [{
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "difficulty": t.difficulty,
            "course_id": t.course_id
        } for t in topics]
    }

@router.get("/{topic_id}")
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get topic details with lessons"""
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    lessons = db.query(models.Lesson).filter(models.Lesson.id == topic_id).all()
    assessments = db.query(models.Assessment).filter(models.Assessment.topic_id == topic_id).all()

    return {
        "topic": {
            "id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "difficulty": topic.difficulty,
            "prerequisites": topic.prerequisites
        },
        "lessons": [{
            "id": l.id,
            "title": l.title,
            "description": l.description,
            "duration_minutes": l.duration_minutes
        } for l in lessons],
        "assessments": [{
            "id": a.id,
            "title": a.title,
            "assessment_type": a.assessment_type,
            "passing_score": a.passing_score
        } for a in assessments]
    }

@router.get("/course/{course_id}")
def get_course_topics(course_id: int, db: Session = Depends(get_db)):
    """Get all topics for a course"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    topics = db.query(models.Topic).filter(models.Topic.course_id == course_id).all()

    return {
        "course": {
            "id": course.id,
            "name": course.name
        },
        "topics": [{
            "id": t.id,
            "title": t.title,
            "difficulty": t.difficulty,
            "order": t.order_index
        } for t in sorted(topics, key=lambda x: x.order_index)]
    }

@router.get("/{topic_id}/content")
def get_topic_content(topic_id: int, db: Session = Depends(get_db)):
    """Get complete topic content with all lessons and videos"""
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    lessons = db.query(models.Lesson).filter(models.Lesson.topic_id == topic_id).all()

    content_data = {
        "topic": {
            "id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "difficulty": topic.difficulty
        },
        "lessons": []
    }

    for lesson in lessons:
        videos = db.query(models.Video).filter(models.Video.lesson_id == lesson.id).all()

        lesson_data = {
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description,
            "videos": [{
                "id": v.id,
                "title": v.title,
                "duration_seconds": v.duration_seconds,
                "url": v.url
            } for v in videos]
        }

        content_data["lessons"].append(lesson_data)

    return content_data

@router.get("/{topic_id}/progress")
def get_topic_progress(topic_id: int, student_id: int, db: Session = Depends(get_db)):
    """Get student's progress on a topic"""
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    progress = db.query(models.TopicProgress).filter(
        models.TopicProgress.student_id == student_id,
        models.TopicProgress.topic_id == topic_id
    ).first()

    if not progress:
        return {
            "topic_id": topic_id,
            "student_id": student_id,
            "status": "not_started",
            "mastery_level": 0.0,
            "time_spent": 0,
            "attempts": 0
        }

    return {
        "topic_id": topic_id,
        "student_id": student_id,
        "status": progress.status,
        "mastery_level": progress.mastery_level,
        "time_spent": progress.time_spent,
        "attempts": progress.attempts,
        "best_score": progress.best_score,
        "completed_at": progress.completed_at
    }
