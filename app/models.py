from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    current_topic = Column(String, nullable=False)
    completed_topics = Column(Integer, default=0)
    assessments_taken = Column(Integer, default=0)
    strong_area = Column(String, default="")
    weak_area = Column(String, default="")
    mastery = Column(Float, default=0.0)
    is_logged_in = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    performance_records = relationship("PerformanceData", back_populates="student")
    knowledge_state = relationship("KnowledgeState", back_populates="student", uselist=False)
    path_history = relationship("PathVersion", back_populates="student")
    teacher_overrides = relationship("TeacherOverride", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    subject = Column(String, nullable=False)
    expertise_areas = Column(JSON, default=[])  # List of expertise areas
    courses_taught = Column(Integer, default=0)
    students_managed = Column(Integer, default=0)
    experience_years = Column(Integer, default=0)
    qualification = Column(String, default="")
    phone = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class KnowledgeState(Base):
    """Maintains structured representation of what each student knows"""
    __tablename__ = "knowledge_state"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True)
    knowledge_map = Column(JSON, default={})  # Topic -> mastery level mapping
    skill_profile = Column(JSON, default={})  # Skills and proficiency levels
    learning_pace = Column(Float, default=1.0)  # Topics per day
    optimal_difficulty = Column(String, default="medium")
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="knowledge_state")

class PerformanceData(Base):
    """Continuous data ingestion from assessments, attendance, engagement, doubts"""
    __tablename__ = "performance_data"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))

    # Assessment data
    assessment_score = Column(Float, nullable=True)  # 0-100
    assessment_type = Column(String, default="")  # quiz, exam, coding_challenge

    # Attendance data
    attendance_status = Column(String, default="")  # present, absent, excused
    session_duration = Column(Float, default=0.0)  # minutes

    # Engagement data
    interaction_count = Column(Integer, default=0)  # clicks, scrolls, etc.
    time_on_topic = Column(Float, default=0.0)  # minutes
    resource_type = Column(String, default="")  # video, article, interactive

    # Doubt/Question data
    doubts_asked = Column(Integer, default=0)
    doubts_resolved = Column(Integer, default=0)
    question_difficulty = Column(String, default="")  # easy, medium, hard

    topic_name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="performance_records")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    topic = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)  # easy, medium, hard
    reason = Column(Text, nullable=False)
    reasons_list = Column(JSON, default=[])  # Detailed reasons
    confidence_score = Column(Float, default=0.0)
    skill_area = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class TopicProgress(Base):
    __tablename__ = "topic_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    topic_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # Completed, Current, Locked, In Progress
    mastery_level = Column(Float, default=0.0)  # 0-1
    time_spent = Column(Float, default=0.0)  # minutes
    completed_at = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)
    best_score = Column(Float, default=0.0)

    # Relationships
    topic = relationship("Topic", back_populates="progress")

class PathVersion(Base):
    """Stores historical path decisions for audit and model improvement"""
    __tablename__ = "path_versions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    version_number = Column(Integer, nullable=False)
    previous_topic = Column(String, nullable=True)
    recommended_topic = Column(String, nullable=False)
    actual_difficulty = Column(String, default="medium")
    decision_reasoning = Column(JSON, default={})
    version_timestamp = Column(DateTime, default=datetime.utcnow)
    performance_before = Column(Float, default=0.0)  # mastery before
    performance_after = Column(Float, default=0.0)  # mastery after
    was_optimal = Column(Boolean, default=None)  # Did this lead to good learning?
    student = relationship("Student", back_populates="path_history")

class TeacherOverride(Base):
    """Teacher overrides feed back into the model"""
    __tablename__ = "teacher_overrides"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    original_recommendation = Column(String, nullable=False)
    override_to_topic = Column(String, nullable=False)
    override_to_difficulty = Column(String, default="medium")
    reason = Column(Text, nullable=False)
    teacher_notes = Column(Text, default="")
    timestamp = Column(DateTime, default=datetime.utcnow)
    effectiveness_rating = Column(Float, nullable=True)  # 0-1, how well did it work

    student = relationship("Student", back_populates="teacher_overrides")

class DifficultyLog(Base):
    """Logs difficulty calibration decisions"""
    __tablename__ = "difficulty_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    topic = Column(String, nullable=False)
    previous_difficulty = Column(String, default="medium")
    new_difficulty = Column(String, default="medium")
    trigger_metric = Column(String, nullable=False)  # e.g., "score_too_high", "engagement_low"
    score_before = Column(Float, default=0.0)
    score_after = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

# ==================== COURSE STRUCTURE ====================

class Course(Base):
    """Learning courses with complete curriculum"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, default="")
    category = Column(String, nullable=False)  # Programming, Web Dev, AI/ML, Data, Cloud, Design
    level = Column(String, default="beginner")  # beginner, intermediate, advanced
    duration_weeks = Column(Integer, default=0)
    icon = Column(String, default="")
    color = Column(String, default="#3B82F6")
    students_enrolled = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    concepts = relationship("Concept", back_populates="course", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="course", cascade="all, delete-orphan")
    student_progress = relationship("StudentProgress", back_populates="course", cascade="all, delete-orphan")

class Concept(Base):
    """Course-specific concepts (no sharing between courses)"""
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="concepts")
    topics = relationship("Topic", back_populates="concept")
    formulas = relationship("Formula", back_populates="concept", cascade="all, delete-orphan")

class Topic(Base):
    """Topics within concepts"""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    difficulty = Column(String, default="beginner")  # beginner, intermediate, advanced
    order_index = Column(Integer, default=0)
    prerequisites = Column(JSON, default=[])  # List of prerequisite topic IDs
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="topics")
    concept = relationship("Concept", back_populates="topics")
    lessons = relationship("Lesson", back_populates="topic", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="topic", cascade="all, delete-orphan")
    progress = relationship("TopicProgress", back_populates="topic", cascade="all, delete-orphan")

class Lesson(Base):
    """Lessons within topics"""
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    order_index = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    topic = relationship("Topic", back_populates="lessons")
    videos = relationship("Video", back_populates="lesson", cascade="all, delete-orphan")

class Video(Base):
    """Video content with tracking"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    url = Column(String, nullable=False)
    duration_seconds = Column(Integer, default=0)
    has_subtitles = Column(Boolean, default=False)
    resolution_options = Column(JSON, default=["720p", "1080p"])
    topic = Column(String, default="general")  # New field for topic category
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    lesson = relationship("Lesson", back_populates="videos")
    concepts = relationship("VideoConcept", back_populates="video", cascade="all, delete-orphan")
    subtitles = relationship("Subtitle", back_populates="video", cascade="all, delete-orphan")
    watch_history = relationship("VideoWatchHistory", back_populates="video", cascade="all, delete-orphan")
    sessions = relationship("VideoSession", back_populates="video", cascade="all, delete-orphan")

class VideoConcept(Base):
    """Concepts explained in videos"""
    __tablename__ = "video_concepts"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    explanation = Column(Text, default="")
    real_world_example = Column(Text, default="")
    order_index = Column(Integer, default=0)

    # Relationships
    video = relationship("Video", back_populates="concepts")
    formulas = relationship("Formula", back_populates="video_concept")

class Formula(Base):
    """Mathematical formulas with explanations"""
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    video_concept_id = Column(Integer, ForeignKey("video_concepts.id"), nullable=True)
    name = Column(String, nullable=False)
    latex_formula = Column(String, nullable=False)  # LaTeX representation
    plain_text = Column(String, default="")
    explanation = Column(Text, default="")
    use_case = Column(Text, default="")
    real_world_example = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    concept = relationship("Concept", back_populates="formulas")
    video_concept = relationship("VideoConcept", back_populates="formulas")

class Subtitle(Base):
    """Video subtitles in multiple languages"""
    __tablename__ = "subtitles"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    language = Column(String, nullable=False)  # en, hi, es, etc.
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    video = relationship("Video", back_populates="subtitles")

class Assessment(Base):
    """Quizzes and exams for topics"""
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    assessment_type = Column(String, default="quiz")  # quiz, exam, coding_challenge
    passing_score = Column(Float, default=60.0)
    time_limit_minutes = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="assessments")
    topic = relationship("Topic", back_populates="assessments")
    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")
    results = relationship("AssessmentResult", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentQuestion(Base):
    """Questions in assessments"""
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, default="mcq")  # mcq, essay, coding
    options = Column(JSON, default={})  # For MCQ: {A, B, C, D} and correct answer
    correct_answer = Column(String, default="")
    points = Column(Float, default=1.0)
    order_index = Column(Integer, default=0)

    # Relationships
    assessment = relationship("Assessment", back_populates="questions")

class VideoWatchHistory(Base):
    """Track video viewing"""
    __tablename__ = "video_watch_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))
    watch_start_time = Column(DateTime, default=datetime.utcnow)
    watch_end_time = Column(DateTime, nullable=True)
    watch_duration_seconds = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)

    # Relationships
    video = relationship("Video", back_populates="watch_history")

class VideoSession(Base):
    """Track playback sessions (pause/resume)"""
    __tablename__ = "video_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))
    current_position_seconds = Column(Integer, default=0)
    playback_speed = Column(Float, default=1.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    video = relationship("Video", back_populates="sessions")

class StudentProgress(Base):
    """Track student progress in courses"""
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    status = Column(String, default="not_started")  # not_started, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    topics_total = Column(Integer, default=0)
    topics_completed = Column(Integer, default=0)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completion_date = Column(DateTime, nullable=True)

    # Relationships
    course = relationship("Course", back_populates="student_progress")

class AssessmentResult(Base):
    """Store assessment submission results"""
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    score = Column(Float, default=0.0)
    passing_score = Column(Float, default=60.0)
    is_passed = Column(Boolean, default=False)
    answers = Column(JSON, default={})
    time_taken_seconds = Column(Integer, default=0)
    submission_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    assessment = relationship("Assessment", back_populates="results")
