from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from typing import List

router = APIRouter(prefix="/api/v1/courses", tags=["courses"])

@router.get("/")
def get_all_courses(skip: int = 0, limit: int = 100, category: str = None, db: Session = Depends(get_db)):
    """Get all courses with optional filtering"""
    query = db.query(models.Course)

    if category:
        query = query.filter(models.Course.category == category)

    courses = query.offset(skip).limit(limit).all()
    total = db.query(models.Course).count()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "courses": courses
    }

@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get course details by ID"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/{course_id}/roadmap")
def get_course_roadmap(course_id: int, student_id: int = None, db: Session = Depends(get_db)):
    """Get course roadmap with topics and concepts"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    concepts = db.query(models.Concept).filter(models.Concept.course_id == course_id).all()
    topics = db.query(models.Topic).filter(models.Topic.course_id == course_id).all()

    roadmap = {
        "course": {
            "id": course.id,
            "name": course.name,
            "description": course.description,
            "category": course.category,
            "level": course.level,
            "duration_weeks": course.duration_weeks
        },
        "concepts": [{"id": c.id, "name": c.name, "order": c.order_index} for c in concepts],
        "topics": [{"id": t.id, "title": t.title, "difficulty": t.difficulty, "order": t.order_index} for t in topics]
    }

    if student_id:
        # Add student progress
        progress = db.query(models.StudentProgress).filter(
            models.StudentProgress.student_id == student_id,
            models.StudentProgress.course_id == course_id
        ).first()

        if progress:
            roadmap["student_progress"] = {
                "status": progress.status,
                "progress_percentage": progress.progress_percentage,
                "enrollment_date": progress.enrollment_date
            }

    return roadmap

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all available course categories"""
    categories = db.query(models.Course.category).distinct().all()
    return {"categories": [c[0] for c in categories]}
