from sqlalchemy.orm import Session
from app.models import (
    Student, Recommendation, TopicProgress, KnowledgeState,
    PerformanceData, PathVersion
)
from datetime import datetime

def seed_data(db: Session):
    if db.query(Student).first():
        return

    # ==================== Create Students ====================
    students = [
        Student(
            name="Rahul",
            email="rahul@example.com",
            current_topic="Control Statements",
            completed_topics=2,
            assessments_taken=3,
            strong_area="Variables and Data Types",
            weak_area="Logic Building",
            mastery=0.62,
            is_logged_in=True,
            is_active=True
        ),
        Student(
            name="Anjali",
            email="anjali@example.com",
            current_topic="Functions",
            completed_topics=3,
            assessments_taken=4,
            strong_area="Control Statements",
            weak_area="OOP",
            mastery=0.78,
            is_logged_in=True,
            is_active=False
        ),
        Student(
            name="Kiran",
            email="kiran@example.com",
            current_topic="Variables and Data Types",
            completed_topics=1,
            assessments_taken=2,
            strong_area="Basics",
            weak_area="Control Statements",
            mastery=0.45,
            is_logged_in=False,
            is_active=False
        )
    ]

    db.add_all(students)
    db.commit()

    # Fetch students for further references
    rahul = db.query(Student).filter(Student.email == "rahul@example.com").first()
    anjali = db.query(Student).filter(Student.email == "anjali@example.com").first()
    kiran = db.query(Student).filter(Student.email == "kiran@example.com").first()

    # ==================== Create Recommendations ====================
    recs = [
        Recommendation(
            student_id=rahul.id,
            topic="Control Statements",
            difficulty="medium",
            reason="Need more practice in logic building",
            reasons_list=[
                "You have a strong foundation in prerequisites for Control Statements",
                "Problem difficulty matches your current level (medium)",
                "Aligned with your learning pace and progress goals",
                "This will help strengthen your weak area in Logic Building"
            ],
            confidence_score=0.85,
            skill_area="Logic Building"
        ),
        Recommendation(
            student_id=anjali.id,
            topic="Functions",
            difficulty="medium",
            reason="Ready for function-based problems",
            reasons_list=[
                "You have a strong foundation in prerequisites for Functions",
                "Problem difficulty matches your current level (medium)",
                "Your recent strong performance indicates readiness for new content",
                "Functions build on your strong foundation in Control Statements"
            ],
            confidence_score=0.92,
            skill_area="Modularity"
        ),
        Recommendation(
            student_id=kiran.id,
            topic="Variables and Data Types",
            difficulty="easy",
            reason="Needs stronger basics before moving ahead",
            reasons_list=[
                "Building a strong foundation is crucial for your progress",
                "Starting with easy problems will build confidence",
                "Master the basics to progress to more advanced topics",
                "Your pace suggests taking time with fundamentals"
            ],
            confidence_score=0.88,
            skill_area="Basics"
        )
    ]

    db.add_all(recs)
    db.commit()

    # ==================== Create Topic Progress ====================
    progress_rows = [
        # Rahul's progress
        TopicProgress(student_id=rahul.id, topic_name="Introduction to Python", status="Completed", mastery_level=0.95, time_spent=120, best_score=95),
        TopicProgress(student_id=rahul.id, topic_name="Variables and Data Types", status="Completed", mastery_level=0.85, time_spent=150, best_score=88),
        TopicProgress(student_id=rahul.id, topic_name="Control Statements", status="In Progress", mastery_level=0.60, time_spent=90, best_score=75),
        TopicProgress(student_id=rahul.id, topic_name="Functions", status="Locked", mastery_level=0.0),

        # Anjali's progress
        TopicProgress(student_id=anjali.id, topic_name="Introduction to Python", status="Completed", mastery_level=1.0, time_spent=100, best_score=100),
        TopicProgress(student_id=anjali.id, topic_name="Variables and Data Types", status="Completed", mastery_level=0.95, time_spent=120, best_score=96),
        TopicProgress(student_id=anjali.id, topic_name="Control Statements", status="Completed", mastery_level=0.92, time_spent=130, best_score=94),
        TopicProgress(student_id=anjali.id, topic_name="Functions", status="In Progress", mastery_level=0.75, time_spent=80, best_score=82),

        # Kiran's progress
        TopicProgress(student_id=kiran.id, topic_name="Introduction to Python", status="Completed", mastery_level=0.80, time_spent=180, best_score=82),
        TopicProgress(student_id=kiran.id, topic_name="Variables and Data Types", status="In Progress", mastery_level=0.45, time_spent=100, best_score=45),
        TopicProgress(student_id=kiran.id, topic_name="Control Statements", status="Locked", mastery_level=0.0)
    ]

    db.add_all(progress_rows)
    db.commit()

    # ==================== Create Knowledge State ====================
    knowledge_states = [
        KnowledgeState(
            student_id=rahul.id,
            knowledge_map={
                "Introduction to Python": 0.95,
                "Variables and Data Types": 0.85,
                "Control Statements": 0.60,
                "Functions": 0.0
            },
            skill_profile={"Basics": 0.90, "Logic Building": 0.60, "Modularity": 0.0},
            learning_pace=1.2,
            optimal_difficulty="medium"
        ),
        KnowledgeState(
            student_id=anjali.id,
            knowledge_map={
                "Introduction to Python": 1.0,
                "Variables and Data Types": 0.95,
                "Control Statements": 0.92,
                "Functions": 0.75
            },
            skill_profile={"Basics": 0.96, "Logic Building": 0.92, "Modularity": 0.75},
            learning_pace=1.5,
            optimal_difficulty="medium"
        ),
        KnowledgeState(
            student_id=kiran.id,
            knowledge_map={
                "Introduction to Python": 0.80,
                "Variables and Data Types": 0.45,
                "Control Statements": 0.0,
                "Functions": 0.0
            },
            skill_profile={"Basics": 0.60, "Logic Building": 0.0, "Modularity": 0.0},
            learning_pace=0.8,
            optimal_difficulty="easy"
        )
    ]

    db.add_all(knowledge_states)
    db.commit()

    # ==================== Create Performance Data ====================
    performance_data = [
        # Rahul's recent performance
        PerformanceData(student_id=rahul.id, assessment_score=75, assessment_type="quiz", topic_name="Control Statements", time_on_topic=45, interaction_count=15),
        PerformanceData(student_id=rahul.id, assessment_score=82, assessment_type="exam", topic_name="Variables and Data Types", time_on_topic=60, interaction_count=25),

        # Anjali's recent performance
        PerformanceData(student_id=anjali.id, assessment_score=94, assessment_type="quiz", topic_name="Control Statements", time_on_topic=30, interaction_count=20),
        PerformanceData(student_id=anjali.id, assessment_score=82, assessment_type="exam", topic_name="Functions", time_on_topic=50, interaction_count=30),

        # Kiran's recent performance
        PerformanceData(student_id=kiran.id, assessment_score=45, assessment_type="quiz", topic_name="Variables and Data Types", time_on_topic=90, interaction_count=35),
        PerformanceData(student_id=kiran.id, assessment_score=38, assessment_type="exam", topic_name="Variables and Data Types", time_on_topic=75, interaction_count=28),
    ]

    db.add_all(performance_data)
    db.commit()

    # ==================== Create Path Versions ====================
    path_versions = [
        PathVersion(
            student_id=rahul.id,
            version_number=1,
            previous_topic="Variables and Data Types",
            recommended_topic="Control Statements",
            actual_difficulty="medium",
            decision_reasoning={"based_on": "mastery_score", "threshold": 0.70},
            performance_before=0.62,
            performance_after=0.65
        ),
        PathVersion(
            student_id=anjali.id,
            version_number=1,
            previous_topic="Control Statements",
            recommended_topic="Functions",
            actual_difficulty="medium",
            decision_reasoning={"based_on": "mastery_score", "threshold": 0.85},
            performance_before=0.75,
            performance_after=0.78
        ),
        PathVersion(
            student_id=kiran.id,
            version_number=1,
            previous_topic="Introduction to Python",
            recommended_topic="Variables and Data Types",
            actual_difficulty="easy",
            decision_reasoning={"based_on": "learning_pace", "adjusted": True},
            performance_before=0.45,
            performance_after=0.45
        )
    ]

    db.add_all(path_versions)
    db.commit()
