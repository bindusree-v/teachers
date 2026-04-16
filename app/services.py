from sqlalchemy.orm import Session
from app.models import (
    Student, Recommendation, TopicProgress, PerformanceData,
    KnowledgeState, PathVersion, TeacherOverride, DifficultyLog,
    Course, Topic, Video, StudentProgress, AssessmentResult, Assessment
)
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# ==================== RECOMMENDATION ENGINE ====================

class RecommendationEngine:
    """Determines the next best learning action for each student"""

    # Curriculum structure - prerequisite chain
    CURRICULUM = [
        "Introduction to Python",
        "Variables and Data Types",
        "Control Statements",
        "Functions",
        "Object-Oriented Programming",
        "Data Structures",
        "Algorithms",
        "Advanced Topics"
    ]

    TOPICS_BY_SKILL = {
        "Variables and Data Types": ["Basics"],
        "Control Statements": ["Logic Building"],
        "Functions": ["Modularity"],
        "Object-Oriented Programming": ["OOP"],
        "Data Structures": ["Problem Solving"],
        "Algorithms": ["Algorithm Design"],
    }

    @staticmethod
    def get_next_recommended_topic(db: Session, student_id: int) -> Dict:
        """
        Generates next best topic recommendation using multiple factors:
        - Student mastery levels
        - Learning pace
        - Performance metrics
        - Knowledge gaps
        """
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None

        # Get student's knowledge state
        knowledge_state = db.query(KnowledgeState).filter(
            KnowledgeState.student_id == student_id
        ).first()

        # Get recent performance data
        recent_perf = db.query(PerformanceData).filter(
            PerformanceData.student_id == student_id
        ).order_by(PerformanceData.timestamp.desc()).limit(10).all()

        # Get current progress
        topics = db.query(TopicProgress).filter(
            TopicProgress.student_id == student_id
        ).all()

        # Calculate scores
        mastery_scores = RecommendationEngine._calculate_mastery_scores(
            student, topics, recent_perf
        )

        # Find next optimal topic
        next_topic = RecommendationEngine._find_next_topic(
            student, mastery_scores, topics
        )

        # Calculate difficulty
        difficulty = RecommendationEngine._calculate_optimal_difficulty(
            student, next_topic, mastery_scores
        )

        # Generate reasons
        reasons = RecommendationEngine._generate_reasons(
            student, next_topic, mastery_scores, recent_perf
        )

        return {
            "topic": next_topic,
            "difficulty": difficulty,
            "reasons": reasons,
            "skill_area": RecommendationEngine.TOPICS_BY_SKILL.get(next_topic, ["General"])[0],
            "confidence_score": min(mastery_scores.get(next_topic, 0.5) + 0.2, 1.0)
        }

    @staticmethod
    def _calculate_mastery_scores(student, topics, recent_perf) -> Dict[str, float]:
        """Calculate mastery score for each topic"""
        scores = {}

        for topic in RecommendationEngine.CURRICULUM:
            topic_progress = next((t for t in topics if t.topic_name == topic), None)

            if topic_progress:
                base_score = topic_progress.mastery_level
            else:
                base_score = 0.0

            # Adjust based on recent performance
            relevant_perf = [p for p in recent_perf if p.topic_name == topic]
            if relevant_perf:
                avg_score = sum(p.assessment_score or 0 for p in relevant_perf) / len(relevant_perf)
                base_score = (base_score + avg_score / 100) / 2

            scores[topic] = min(base_score, 1.0)

        return scores

    @staticmethod
    def _find_next_topic(student, mastery_scores: Dict[str, float], topics) -> str:
        """Find optimal next topic based on prerequisites and mastery"""
        current_idx = 0

        # Find current topic index
        for idx, topic in enumerate(RecommendationEngine.CURRICULUM):
            if topic == student.current_topic:
                current_idx = idx
                break

        # Check if can move to next topic
        if current_idx < len(RecommendationEngine.CURRICULUM) - 1:
            current_mastery = mastery_scores.get(student.current_topic, 0.5)

            # Need 60% mastery to progress
            if current_mastery >= 0.6:
                return RecommendationEngine.CURRICULUM[current_idx + 1]

        # If not progressing, stay on current or recommend practice
        return student.current_topic

    @staticmethod
    def _calculate_optimal_difficulty(student, topic: str, mastery_scores) -> str:
        """Calculate optimal difficulty for the topic"""
        mastery = mastery_scores.get(topic, 0.5)

        if mastery < 0.4:
            return "easy"
        elif mastery < 0.7:
            return "medium"
        else:
            return "hard"

    @staticmethod
    def _generate_reasons(student, topic: str, mastery_scores, recent_perf) -> List[str]:
        """Generate detailed reasons for recommendation"""
        reasons = []

        # Reason 1: Strong area
        if mastery_scores.get(topic, 0) > 0.7:
            reasons.append(f"You have a strong foundation in prerequisites for {topic}")

        # Reason 2: Optimal difficulty
        difficulty = RecommendationEngine._calculate_optimal_difficulty(
            student, topic, mastery_scores
        )
        reasons.append(f"Problem difficulty matches your current level ({difficulty})")

        # Reason 3: Learning pace
        reasons.append("Aligned with your learning pace and progress goals")

        # Reason 4: Weakness improvement
        if student.weak_area:
            if any(weak in topic for weak in student.weak_area.split()):
                reasons.append(f"This will help strengthen your weak area in {student.weak_area}")

        # Reason 5: Recent performance
        if recent_perf and recent_perf[0].assessment_score and recent_perf[0].assessment_score > 75:
            reasons.append("Your recent strong performance indicates readiness for new content")

        return reasons[:4]  # Return top 4 reasons

# ==================== DIFFICULTY CALIBRATION ====================

class DifficultyCalibration:
    """Dynamically adjusts content complexity based on student performance"""

    @staticmethod
    def calibrate_difficulty(db: Session, student_id: int, topic: str) -> str:
        """
        Adjusts difficulty based on performance metrics:
        - Assessment scores
        - Time spent
        - Engagement level
        - Error patterns
        """
        student = db.query(Student).filter(Student.id == student_id).first()

        # Get recent performance
        recent_performance = db.query(PerformanceData).filter(
            PerformanceData.student_id == student_id,
            PerformanceData.topic_name == topic
        ).order_by(PerformanceData.timestamp.desc()).limit(5).all()

        if not recent_performance:
            return "medium"

        # Calculate metrics
        avg_score = sum(p.assessment_score or 0 for p in recent_performance) / len(recent_performance)
        avg_time = sum(p.time_on_topic or 0 for p in recent_performance) / len(recent_performance)
        engagement = sum(p.interaction_count or 0 for p in recent_performance) / len(recent_performance)

        # Calibration logic
        new_difficulty = "medium"
        trigger_metric = "stable"

        if avg_score > 85 and avg_time < 30:  # Too easy, too fast
            new_difficulty = "hard"
            trigger_metric = "score_too_high"
        elif avg_score > 80 and avg_time < 45:
            new_difficulty = "hard"
            trigger_metric = "score_high_speed"
        elif avg_score < 40:  # Too hard
            new_difficulty = "easy"
            trigger_metric = "score_too_low"
        elif avg_score < 50 and avg_time > 60:  # Struggling
            new_difficulty = "easy"
            trigger_metric = "struggling"
        elif engagement < 10:  # Low engagement
            new_difficulty = "easy"
            trigger_metric = "engagement_low"

        # Log the calibration
        if recent_performance:
            old_diff = DifficultyCalibration._get_current_difficulty(
                db, student_id, topic
            )
            DifficultyCalibration._log_difficulty_change(
                db, student_id, topic, old_diff, new_difficulty,
                trigger_metric, recent_performance[0].assessment_score or 0
            )

        return new_difficulty

    @staticmethod
    def _get_current_difficulty(db: Session, student_id: int, topic: str) -> str:
        """Get current difficulty level"""
        rec = db.query(Recommendation).filter(
            Recommendation.student_id == student_id
        ).order_by(Recommendation.created_at.desc()).first()

        if rec and rec.is_active:
            return rec.difficulty
        return "medium"

    @staticmethod
    def _log_difficulty_change(db: Session, student_id: int, topic: str,
                               old_diff: str, new_diff: str, trigger: str, score: float):
        """Log difficulty calibration change"""
        log = DifficultyLog(
            student_id=student_id,
            topic=topic,
            previous_difficulty=old_diff,
            new_difficulty=new_diff,
            trigger_metric=trigger,
            score_before=score
        )
        db.add(log)
        db.commit()

# ==================== DATA INGESTION PIPELINE ====================

class DataIngestionPipeline:
    """Continuous data ingestion from all platform modules"""

    @staticmethod
    def ingest_assessment_data(db: Session, student_id: int, topic: str,
                              score: float, assessment_type: str = "quiz"):
        """Ingest assessment data"""
        perf_data = PerformanceData(
            student_id=student_id,
            assessment_score=score,
            assessment_type=assessment_type,
            topic_name=topic
        )
        db.add(perf_data)

        # Update student mastery
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            student.mastery = (student.mastery + score / 100) / 2
            student.assessments_taken += 1

        db.commit()
        return perf_data

    @staticmethod
    def ingest_attendance_data(db: Session, student_id: int,
                              status: str, session_duration: float):
        """Ingest attendance data"""
        perf_data = PerformanceData(
            student_id=student_id,
            attendance_status=status,
            session_duration=session_duration,
            topic_name="General"
        )
        db.add(perf_data)
        db.commit()
        return perf_data

    @staticmethod
    def ingest_engagement_data(db: Session, student_id: int, topic: str,
                              interaction_count: int, time_on_topic: float,
                              resource_type: str):
        """Ingest engagement data"""
        perf_data = PerformanceData(
            student_id=student_id,
            interaction_count=interaction_count,
            time_on_topic=time_on_topic,
            resource_type=resource_type,
            topic_name=topic
        )
        db.add(perf_data)
        db.commit()
        return perf_data

    @staticmethod
    def ingest_doubt_data(db: Session, student_id: int, topic: str,
                         doubts_asked: int, doubts_resolved: int,
                         question_difficulty: str):
        """Ingest doubt/question data"""
        perf_data = PerformanceData(
            student_id=student_id,
            doubts_asked=doubts_asked,
            doubts_resolved=doubts_resolved,
            question_difficulty=question_difficulty,
            topic_name=topic
        )
        db.add(perf_data)
        db.commit()
        return perf_data

    @staticmethod
    def update_knowledge_state(db: Session, student_id: int):
        """Update student's knowledge state model"""
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None

        knowledge_state = db.query(KnowledgeState).filter(
            KnowledgeState.student_id == student_id
        ).first()

        if not knowledge_state:
            knowledge_state = KnowledgeState(student_id=student_id)
            db.add(knowledge_state)

        # Build knowledge map from topic progress
        topics = db.query(TopicProgress).filter(
            TopicProgress.student_id == student_id
        ).all()

        knowledge_map = {}
        for topic in topics:
            knowledge_map[topic.topic_name] = topic.mastery_level

        knowledge_state.knowledge_map = knowledge_map
        knowledge_state.optimal_difficulty = RecommendationEngine._calculate_optimal_difficulty(
            student, student.current_topic, knowledge_map
        )

        db.commit()
        return knowledge_state

# ==================== TEACHER OVERRIDE & FEEDBACK ====================

class TeacherFeedbackLoop:
    """Teacher overrides feed back into the model"""

    @staticmethod
    def apply_teacher_override(db: Session, student_id: int,
                              original_topic: str, override_topic: str,
                              override_difficulty: str, reason: str,
                              teacher_notes: str = "") -> Dict:
        """Apply teacher override and update learning path"""

        # Create override record
        override = TeacherOverride(
            student_id=student_id,
            original_recommendation=original_topic,
            override_to_topic=override_topic,
            override_to_difficulty=override_difficulty,
            reason=reason,
            teacher_notes=teacher_notes
        )
        db.add(override)

        # Update student's current topic
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            student.current_topic = override_topic

        # Create new path version
        PathVersion._create_path_version(
            db, student_id, original_topic, override_topic,
            override_difficulty, {"override_by_teacher": True, "reason": reason}
        )

        db.commit()
        return {
            "success": True,
            "override_id": override.id,
            "message": f"Overridden to {override_topic}"
        }

    @staticmethod
    def rate_override_effectiveness(db: Session, override_id: int,
                                    effectiveness: float) -> Dict:
        """Rate how effective a teacher override was"""
        override = db.query(TeacherOverride).filter(
            TeacherOverride.id == override_id
        ).first()

        if override:
            override.effectiveness_rating = effectiveness
            db.commit()
            return {
                "success": True,
                "message": "Override effectiveness recorded"
            }

        return {
            "success": False,
            "message": "Override not found"
        }

# ==================== PATH VERSIONING ====================

class PathVersioning:
    """Stores historical path decisions for audit and model improvement"""

    @staticmethod
    def _create_path_version(db: Session, student_id: int,
                            previous_topic: Optional[str],
                            recommended_topic: str,
                            difficulty: str,
                            reasoning: Dict):
        """Create a new path version entry"""

        student = db.query(Student).filter(Student.id == student_id).first()

        # Get latest version number
        latest = db.query(PathVersion).filter(
            PathVersion.student_id == student_id
        ).order_by(PathVersion.version_number.desc()).first()

        version_num = (latest.version_number + 1) if latest else 1

        path_version = PathVersion(
            student_id=student_id,
            version_number=version_num,
            previous_topic=previous_topic,
            recommended_topic=recommended_topic,
            actual_difficulty=difficulty,
            decision_reasoning=reasoning,
            performance_before=student.mastery if student else 0.0
        )
        db.add(path_version)
        db.commit()
        return path_version

    @staticmethod
    def get_path_history(db: Session, student_id: int, limit: int = 20) -> List[Dict]:
        """Get student's learning path history"""
        versions = db.query(PathVersion).filter(
            PathVersion.student_id == student_id
        ).order_by(PathVersion.version_number.desc()).limit(limit).all()

        return [
            {
                "version": v.version_number,
                "from_topic": v.previous_topic,
                "to_topic": v.recommended_topic,
                "difficulty": v.actual_difficulty,
                "timestamp": v.version_timestamp.isoformat(),
                "was_optimal": v.was_optimal,
                "performance_change": v.performance_after - v.performance_before
            }
            for v in versions
        ]

# ==================== DASHBOARD SERVICES ====================

def get_student_dashboard(db: Session, student_id: int):
    """Get comprehensive student dashboard data"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None

    topics = db.query(TopicProgress).filter(TopicProgress.student_id == student_id).all()
    recommendation = db.query(Recommendation).filter(
        Recommendation.student_id == student_id,
        Recommendation.is_active == True
    ).order_by(Recommendation.created_at.desc()).first()

    learning_path = [topic.topic_name for topic in topics]
    completed_topics = [t.topic_name for t in topics if t.status == "Completed"]

    return {
        "student_name": student.name,
        "mastery": student.mastery,
        "current_topic": student.current_topic,
        "completed_topics": len(completed_topics),
        "assessments_taken": student.assessments_taken,
        "strong_area": student.strong_area,
        "weak_area": student.weak_area,
        "learning_path": learning_path,
        "recommendation": {
            "topic": recommendation.topic if recommendation else "No recommendation",
            "difficulty": recommendation.difficulty if recommendation else "N/A",
            "reasons": recommendation.reasons_list if recommendation else [],
            "skill_area": recommendation.skill_area if recommendation else "" ,
        },
        "last_updated": student.updated_at.isoformat()
    }

def get_teacher_dashboard(db: Session):
    """Get teacher dashboard with all students and course analytics"""
    try:
        students = db.query(Student).all()
        total = len(students)
        active = len([s for s in students if s.is_active])
        inactive = total - active

        # Get course analytics
        courses = db.query(Course).all()
        course_analytics = []
        
        for course in courses:
            # Get topics for this course
            topics = db.query(Topic).filter(Topic.course_id == course.id).all()
            topic_ids = [t.id for t in topics]

            # Get assessments for this course
            assessments = db.query(Assessment).filter(Assessment.course_id == course.id).all()

            # Get videos for this course
            videos = db.query(Video).filter(Video.topic.in_([t.title for t in topics])).all() if topics else []

            # Get student progress for this course - safely
            student_progress = []
            try:
                student_progress = db.query(StudentProgress).filter(StudentProgress.course_id == course.id).all()
            except:
                student_progress = []

            enrolled_students = len(student_progress)
            completed_students = len([p for p in student_progress if p.status == 'completed']) if student_progress else 0

            # Get assessment results for this course - safely
            assessment_results = []
            try:
                assessment_results = db.query(AssessmentResult).filter(
                    AssessmentResult.assessment_id.in_([a.id for a in assessments])
                ).all() if assessments else []
            except:
                assessment_results = []

            # Get attendance data
            attendance_records = []
            try:
                attendance_records = db.query(PerformanceData).filter(
                    PerformanceData.topic_name.in_([t.title for t in topics])
                ).all() if topics else []
            except:
                attendance_records = []

            # Calculate average mastery
            avg_mastery = 0
            if enrolled_students > 0 and student_progress:
                try:
                    avg_mastery = sum([p.progress_percentage for p in student_progress if hasattr(p, 'progress_percentage')]) / enrolled_students
                except:
                    avg_mastery = 0

            course_analytics.append({
                "course_id": course.id,
                "course_name": course.name,
                "enrolled_students": enrolled_students,
                "completed_students": completed_students,
                "total_topics": len(topics),
                "total_assessments": len(assessments),
                "total_videos": len(videos),
                "total_assessment_submissions": len(assessment_results),
                "attendance_count": len(attendance_records),
                "average_mastery": avg_mastery
            })

        return {
            "total_students": total,
            "active_students": active,
            "inactive_students": inactive,
            "students": [
                {
                    "id": s.id,
                    "name": s.name,
                    "current_topic": s.current_topic,
                    "mastery": s.mastery,
                    "weak_area": s.weak_area,
                    "is_logged_in": s.is_logged_in,
                    "is_active": s.is_active
                }
                for s in students
            ],
            "course_analytics": course_analytics
        }
    except Exception as e:
        print(f"Error in get_teacher_dashboard: {e}")
        return {
            "total_students": 0,
            "active_students": 0,
            "inactive_students": 0,
            "students": [],
            "course_analytics": [],
            "error": str(e)
        }

def get_student_analytics(db: Session, student_id: int) -> Dict:
    """Get detailed student analytics"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None

    performance_data = db.query(PerformanceData).filter(
        PerformanceData.student_id == student_id
    ).order_by(PerformanceData.timestamp.desc()).limit(30).all()

    path_history = PathVersioning.get_path_history(db, student_id, limit=10)

    # Calculate statistics
    avg_assessment_score = 0
    total_assessment = 0
    avg_time_on_topic = 0
    total_engagement = 0

    for perf in performance_data:
        if perf.assessment_score:
            avg_assessment_score += perf.assessment_score
            total_assessment += 1
        if perf.time_on_topic:
            avg_time_on_topic += perf.time_on_topic
        total_engagement += perf.interaction_count

    if total_assessment > 0:
        avg_assessment_score /= total_assessment
    if performance_data:
        avg_time_on_topic /= len(performance_data)

    return {
        "student_id": student_id,
        "student_name": student.name,
        "overall_mastery": student.mastery,
        "avg_assessment_score": round(avg_assessment_score, 2),
        "avg_time_on_topic_minutes": round(avg_time_on_topic, 2),
        "total_engagement": total_engagement,
        "path_changes": len(path_history),
        "recent_performance": [
            {
                "timestamp": p.timestamp.isoformat(),
                "topic": p.topic_name,
                "score": p.assessment_score,
                "time_spent": p.time_on_topic,
                "engagement": p.interaction_count
            }
            for p in performance_data[:5]
        ],
        "path_history": path_history
    }
