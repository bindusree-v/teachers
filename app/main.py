from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import Base, engine, get_db, SessionLocal
from app.schemas import (
    StudentDashboardResponse, TeacherDashboardResponse,
    AssessmentDataRequest, AttendanceDataRequest, EngagementDataRequest,
    DoubtDataRequest, PerformanceDataResponse, DifficultyCalibrationResponse,
    RecommendationResponse, TeacherOverrideRequest, TeacherOverrideResponse,
    PathHistoryResponse, StudentAnalyticsResponse, KnowledgeStateResponse,
    BatchPerformanceUpdate, BatchUpdateResponse
)
from app.services import (
    get_student_dashboard, get_teacher_dashboard, get_student_analytics,
    RecommendationEngine, DifficultyCalibration, DataIngestionPipeline,
    TeacherFeedbackLoop, PathVersioning
)
from app.seed import seed_data
from app.routes import courses, videos, assessments, topics

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"⚠️  Warning: Could not create database tables on startup: {e}")
    print("Database tables will be created on first request.")

app = FastAPI(
    title="Adaptive Learning Engine",
    description="AI-powered adaptive learning system with real-time difficulty adjustment",
    version="1.0.0"
)


def ensure_video_schema_compatibility():
    """Apply lightweight schema guards for older databases."""
    try:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE videos ADD COLUMN IF NOT EXISTS topic VARCHAR(50)"))
            conn.execute(text("UPDATE videos SET topic = 'lm' WHERE topic IS NULL"))
    except Exception as e:
        print(f"⚠️  Warning: Could not apply video schema compatibility fixes: {e}")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== STARTUP ====================

@app.on_event("startup")
def startup():
    """Initialize database with seed data"""
    ensure_video_schema_compatibility()
    db = SessionLocal()
    try:
        seed_data(db)
    except Exception as e:
        print(f"⚠️  Note: Seed data not loaded on startup: {e}")
        print("This is OK - seed data will be loaded later via scripts/seed_db.py")
    finally:
        db.close()

# ==================== HEALTH CHECK ====================

@app.get("/")
def home():
    return {"message": "Adaptive Learning Engine Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "adaptive-learning-engine"}

# ==================== LOGIN ENDPOINT ====================

@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    """Get all students for login screen"""
    from app.models import Student
    students = db.query(Student).all()
    return {
        "total": len(students),
        "students": [
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "current_topic": s.current_topic,
                "mastery": s.mastery,
                "is_logged_in": s.is_logged_in,
                "is_active": s.is_active
            }
            for s in students
        ]
    }

@app.post("/login")
def login(student_id: int = None, email: str = None, db: Session = Depends(get_db)):
    """
    Login endpoint - accepts student_id OR email
    Updates is_logged_in = True in database
    Returns student data and token
    """
    from app.models import Student

    student = None
    if student_id:
        student = db.query(Student).filter(Student.id == student_id).first()
    elif email:
        student = db.query(Student).filter(Student.email == email).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update login status in database
    student.is_logged_in = True
    student.is_active = True
    from datetime import datetime
    student.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(student)

    # Log login interaction
    from app.models import PerformanceData
    perf = PerformanceData(
        student_id=student.id,
        topic_name="System",
        resource_type="login",
        interaction_count=1,
        time_on_topic=0
    )
    db.add(perf)
    db.commit()

    return {
        "success": True,
        "student_id": student.id,
        "name": student.name,
        "email": student.email,
        "current_topic": student.current_topic,
        "mastery": student.mastery,
        "is_logged_in": student.is_logged_in,
        "is_active": student.is_active,
        "message": f"Welcome {student.name}! 👋"
    }

@app.post("/logout")
def logout(student_id: int, db: Session = Depends(get_db)):
    """Logout endpoint - sets is_logged_in = False in database"""
    from app.models import Student

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update logout status in database
    student.is_logged_in = False
    from datetime import datetime
    student.updated_at = datetime.utcnow()
    db.commit()

    return {
        "success": True,
        "message": f"Goodbye {student.name}! 👋"
    }

# ==================== STUDENT ENDPOINTS ====================

@app.get("/student/{student_id}", response_model=StudentDashboardResponse)
def student_dashboard(student_id: int, db: Session = Depends(get_db)):
    """Get comprehensive student dashboard"""
    data = get_student_dashboard(db, student_id)
    if not data:
        raise HTTPException(status_code=404, detail="Student not found")
    return data

@app.get("/student/{student_id}/analytics", response_model=StudentAnalyticsResponse)
def student_analytics(student_id: int, db: Session = Depends(get_db)):
    """Get detailed student analytics with performance history"""
    data = get_student_analytics(db, student_id)
    if not data:
        raise HTTPException(status_code=404, detail="Student not found")
    return data

@app.get("/student/{student_id}/knowledge-state", response_model=KnowledgeStateResponse)
def student_knowledge_state(student_id: int, db: Session = Depends(get_db)):
    """Get student's knowledge state model"""
    from app.models import KnowledgeState
    state = db.query(KnowledgeState).filter(KnowledgeState.student_id == student_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="Knowledge state not found")
    return {
        "student_id": student_id,
        "knowledge_map": state.knowledge_map,
        "skill_profile": state.skill_profile,
        "learning_pace": state.learning_pace,
        "optimal_difficulty": state.optimal_difficulty,
        "last_updated": state.last_updated.isoformat()
    }

# ==================== RECOMMENDATION ENGINE ====================

@app.get("/student/{student_id}/recommendation", response_model=RecommendationResponse)
def get_recommendation(student_id: int, db: Session = Depends(get_db)):
    """Get AI-driven recommendation for next best learning action"""
    rec_data = RecommendationEngine.get_next_recommended_topic(db, student_id)
    if not rec_data:
        raise HTTPException(status_code=404, detail="Student not found")

    # Save recommendation to database
    from app.models import Recommendation
    rec = Recommendation(
        student_id=student_id,
        topic=rec_data["topic"],
        difficulty=rec_data["difficulty"],
        reason=" | ".join(rec_data["reasons"]),
        reasons_list=rec_data["reasons"],
        confidence_score=rec_data["confidence_score"],
        skill_area=rec_data["skill_area"] ,
        is_active=True
    )
    db.add(rec)
    db.commit()

    # Create path version
    from app.models import Student
    student = db.query(Student).filter(Student.id == student_id).first()
    PathVersioning._create_path_version(
        db, student_id, student.current_topic,
        rec_data["topic"], rec_data["difficulty"],
        {"based_on": "recommendation_engine"}
    )

    return rec_data

# ==================== DIFFICULTY CALIBRATION ====================

@app.post("/student/{student_id}/calibrate-difficulty/{topic}", response_model=DifficultyCalibrationResponse)
def calibrate_difficulty(student_id: int, topic: str, db: Session = Depends(get_db)):
    """Dynamically calibrate content complexity for student"""
    new_difficulty = DifficultyCalibration.calibrate_difficulty(db, student_id, topic)

    return {
        "student_id": student_id,
        "topic": topic,
        "new_difficulty": new_difficulty,
        "trigger_metric": "calibrated",
        "timestamp": str(datetime.utcnow().isoformat())
    }

# ==================== DATA INGESTION PIPELINE ====================

@app.post("/data/assessment", response_model=PerformanceDataResponse)
def ingest_assessment(data: AssessmentDataRequest, db: Session = Depends(get_db)):
    """Ingest assessment performance data"""
    try:
        from app.models import Student

        # Validate student exists
        student = db.query(Student).filter(Student.id == data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {data.student_id} not found. Please use a valid student ID."
            )

        perf = DataIngestionPipeline.ingest_assessment_data(
            db, data.student_id, data.topic, data.score, data.assessment_type
        )
        return {
            "id": perf.id,
            "student_id": perf.student_id,
            "assessment_score": perf.assessment_score,
            "topic_name": perf.topic_name,
            "timestamp": perf.timestamp.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting assessment: {str(e)}")

@app.post("/data/attendance", response_model=PerformanceDataResponse)
def ingest_attendance(data: AttendanceDataRequest, db: Session = Depends(get_db)):
    """Ingest attendance data"""
    try:
        from app.models import Student

        # Validate student exists
        student = db.query(Student).filter(Student.id == data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {data.student_id} not found. Please use a valid student ID."
            )

        perf = DataIngestionPipeline.ingest_attendance_data(
            db, data.student_id, data.status, data.session_duration
        )
        return {
            "id": perf.id,
            "student_id": perf.student_id,
            "assessment_score": None,
            "topic_name": perf.topic_name,
            "timestamp": perf.timestamp.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting attendance: {str(e)}")

@app.post("/data/engagement", response_model=PerformanceDataResponse)
def ingest_engagement(data: EngagementDataRequest, db: Session = Depends(get_db)):
    """Ingest engagement data"""
    try:
        from app.models import Student

        # Validate student exists
        student = db.query(Student).filter(Student.id == data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {data.student_id} not found. Please use a valid student ID."
            )

        perf = DataIngestionPipeline.ingest_engagement_data(
            db, data.student_id, data.topic,
            data.interaction_count, data.time_on_topic, data.resource_type
        )
        return {
            "id": perf.id,
            "student_id": perf.student_id,
            "assessment_score": None,
            "topic_name": perf.topic_name,
            "timestamp": perf.timestamp.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting engagement: {str(e)}")

@app.post("/data/doubt", response_model=PerformanceDataResponse)
def ingest_doubt(data: DoubtDataRequest, db: Session = Depends(get_db)):
    """Ingest doubt/question data"""
    perf = DataIngestionPipeline.ingest_doubt_data(
        db, data.student_id, data.topic,
        data.doubts_asked, data.doubts_resolved, data.question_difficulty
    )
    return {
        "id": perf.id,
        "student_id": perf.student_id,
        "assessment_score": None,
        "topic_name": perf.topic_name,
        "timestamp": perf.timestamp.isoformat()
    }

@app.post("/data/batch-update", response_model=BatchUpdateResponse)
def batch_update_performance(data: BatchPerformanceUpdate, db: Session = Depends(get_db)):
    """Batch update multiple performance metrics"""
    records_processed = 0

    # Process assessments
    for assessment in data.assessments:
        DataIngestionPipeline.ingest_assessment_data(
            db, data.student_id, assessment.topic,
            assessment.score, assessment.assessment_type
        )
        records_processed += 1

    # Process engagement if provided
    if data.engagement:
        DataIngestionPipeline.ingest_engagement_data(
            db, data.student_id, data.engagement.topic,
            data.engagement.interaction_count,
            data.engagement.time_on_topic,
            data.engagement.resource_type
        )
        records_processed += 1

    # Process attendance if provided
    if data.attendance:
        DataIngestionPipeline.ingest_attendance_data(
            db, data.student_id,
            data.attendance.status,
            data.attendance.session_duration
        )
        records_processed += 1

    # Process doubts if provided
    if data.doubts:
        DataIngestionPipeline.ingest_doubt_data(
            db, data.student_id, data.doubts.topic,
            data.doubts.doubts_asked,
            data.doubts.doubts_resolved,
            data.doubts.question_difficulty
        )
        records_processed += 1

    # Update knowledge state
    DataIngestionPipeline.update_knowledge_state(db, data.student_id)

    # Get updated recommendation
    updated_rec = RecommendationEngine.get_next_recommended_topic(db, data.student_id)

    # Get updated difficulty
    updated_difficulty = DifficultyCalibration.calibrate_difficulty(
        db, data.student_id, updated_rec["topic"]
    )

    return {
        "success": True,
        "student_id": data.student_id,
        "records_processed": records_processed,
        "updated_recommendation": updated_rec,
        "updated_difficulty": updated_difficulty
    }

# ==================== TEACHER ENDPOINTS ====================

@app.get("/teacher/dashboard", response_model=TeacherDashboardResponse)
def teacher_dashboard(db: Session = Depends(get_db)):
    """Get teacher dashboard with all students"""
    return get_teacher_dashboard(db)

@app.post("/teacher/override", response_model=TeacherOverrideResponse)
def teacher_override(override: TeacherOverrideRequest, db: Session = Depends(get_db)):
    """Teacher overrides recommendation (feeds back into model)"""
    result = TeacherFeedbackLoop.apply_teacher_override(
        db, override.student_id, override.original_recommendation,
        override.override_to_topic, override.override_to_difficulty,
        override.reason, override.teacher_notes
    )
    return result

@app.post("/teacher/rate-override")
def rate_override(override_id: int, effectiveness: float, db: Session = Depends(get_db)):
    """Rate effectiveness of a teacher override"""
    result = TeacherFeedbackLoop.rate_override_effectiveness(
        db, override_id, effectiveness
    )
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

# ==================== PATH VERSIONING ====================

@app.get("/student/{student_id}/path-history", response_model=PathHistoryResponse)
def get_path_history(
    student_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get student's learning path history"""
    path_history = PathVersioning.get_path_history(db, student_id, limit)
    if path_history is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "student_id": student_id,
        "path_history": path_history
    }

# ==================== STUDENT LIST ====================

@app.get("/students")
def list_students(db: Session = Depends(get_db)):
    """Get list of all students"""
    from app.models import Student
    students = db.query(Student).all()
    return {
        "total": len(students),
        "students": [
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "current_topic": s.current_topic,
                "mastery": s.mastery,
                "is_active": s.is_active
            }
            for s in students
        ]
    }

# ==================== INCLUDE ROUTERS ====================

app.include_router(courses.router)
app.include_router(topics.router)
app.include_router(videos.router)
app.include_router(assessments.router)

# ==================== ADMIN ENDPOINTS ====================

@app.post("/admin/reset-db")
def reset_database(db: Session = Depends(get_db)):
    """Reset database (development only)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_data(db)
    return {"success": True, "message": "Database reset successfully"}

# ==================== EXPORTS ====================

from datetime import datetime
