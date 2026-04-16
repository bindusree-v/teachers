from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

# ==================== Student Models ====================
class StudentDashboardResponse(BaseModel):
    student_name: str
    mastery: float
    current_topic: str
    completed_topics: int
    assessments_taken: int
    strong_area: str
    weak_area: str
    learning_path: List[str]
    recommendation: dict
    last_updated: str

class StudentBase(BaseModel):
    name: str
    email: str

class StudentDetail(StudentBase):
    id: int
    current_topic: str
    mastery: float
    assessments_taken: int
    strong_area: str
    weak_area: str

# ==================== Teacher Models ====================
class TeacherStudentItem(BaseModel):
    id: int
    name: str
    current_topic: str
    mastery: float
    weak_area: str
    is_logged_in: bool
    is_active: bool

class CourseAnalyticsItem(BaseModel):
    course_id: int
    course_name: str
    enrolled_students: int
    completed_students: int
    total_topics: int
    total_assessments: int
    total_videos: int
    total_assessment_submissions: int
    attendance_count: int
    average_mastery: float

class TeacherDashboardResponse(BaseModel):
    total_students: int
    active_students: int
    inactive_students: int
    students: List[TeacherStudentItem]
    course_analytics: List[CourseAnalyticsItem]

# ==================== Recommendation Models ====================
class RecommendationResponse(BaseModel):
    topic: str
    difficulty: str
    reasons: List[str]
    skill_area: str
    confidence_score: float

class RecommendationDetail(BaseModel):
    id: int
    student_id: int
    topic: str
    difficulty: str
    reasons_list: List[str]
    confidence_score: float
    created_at: str

# ==================== Data Ingestion Models ====================
class AssessmentDataRequest(BaseModel):
    student_id: int
    topic: str
    score: float
    assessment_type: str = "quiz"

class AttendanceDataRequest(BaseModel):
    student_id: int
    status: str  # present, absent, excused
    session_duration: float  # minutes

class EngagementDataRequest(BaseModel):
    student_id: int
    topic: str
    interaction_count: int
    time_on_topic: float  # minutes
    resource_type: str  # video, article, interactive

class DoubtDataRequest(BaseModel):
    student_id: int
    topic: str
    doubts_asked: int
    doubts_resolved: int
    question_difficulty: str

class PerformanceDataResponse(BaseModel):
    id: int
    student_id: int
    assessment_score: Optional[float]
    topic_name: str
    timestamp: str

# ==================== Difficulty Calibration Models ====================
class DifficultyCalibrationResponse(BaseModel):
    student_id: int
    topic: str
    new_difficulty: str
    trigger_metric: str
    timestamp: str

# ==================== Teacher Override Models ====================
class TeacherOverrideRequest(BaseModel):
    student_id: int
    original_recommendation: str
    override_to_topic: str
    override_to_difficulty: str
    reason: str
    teacher_notes: str = ""

class TeacherOverrideResponse(BaseModel):
    success: bool
    override_id: int
    message: str

class OverrideEffectivenessRequest(BaseModel):
    override_id: int
    effectiveness: float  # 0-1

# ==================== Path History Models ====================
class PathVersionResponse(BaseModel):
    version: int
    from_topic: Optional[str]
    to_topic: str
    difficulty: str
    timestamp: str
    was_optimal: Optional[bool]
    performance_change: float

class PathHistoryResponse(BaseModel):
    student_id: int
    path_history: List[PathVersionResponse]

# ==================== Analytics Models ====================
class PerformanceMetric(BaseModel):
    timestamp: str
    topic: str
    score: Optional[float]
    time_spent: float
    engagement: int

class StudentAnalyticsResponse(BaseModel):
    student_id: int
    student_name: str
    overall_mastery: float
    avg_assessment_score: float
    avg_time_on_topic_minutes: float
    total_engagement: int
    path_changes: int
    recent_performance: List[PerformanceMetric]
    path_history: List[PathVersionResponse]

# ==================== Knowledge State Models ====================
class KnowledgeStateResponse(BaseModel):
    student_id: int
    knowledge_map: Dict[str, float]
    skill_profile: Dict[str, float]
    learning_pace: float
    optimal_difficulty: str
    last_updated: str

# ==================== Batch Update Models ====================
class BatchPerformanceUpdate(BaseModel):
    student_id: int
    assessments: List[AssessmentDataRequest] = []
    engagement: Optional[EngagementDataRequest] = None
    attendance: Optional[AttendanceDataRequest] = None
    doubts: Optional[DoubtDataRequest] = None

class BatchUpdateResponse(BaseModel):
    success: bool
    student_id: int
    records_processed: int
    updated_recommendation: Optional[RecommendationResponse]
    updated_difficulty: Optional[str]

# ==================== Auth Models ====================
class AuthSignupRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str  # student | teacher

class AuthLoginRequest(BaseModel):
    email: str
    password: str
    role: str  # student | teacher

class AuthLogoutRequest(BaseModel):
    user_id: int

class AuthResponse(BaseModel):
    success: bool
    message: str
    user_id: int
    username: str
    email: str
    role: str

class AuthRoleStats(BaseModel):
    signup_count: int
    login_count: int
    active_count: int
    inactive_count: int

class AuthStatsResponse(BaseModel):
    students: AuthRoleStats
    teachers: AuthRoleStats
    total_users: int
    updated_at: str
