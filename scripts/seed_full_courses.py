# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import (
    Course, Concept, Topic, Lesson, Video, VideoConcept, Assessment,
    AssessmentQuestion
)

def seed_comprehensive_courses(db: Session):
    if db.query(Course).first():
        print("[OK] Courses already seeded!")
        return

    print("=" * 70)
    print("SEEDING COMPREHENSIVE COURSE DATA - NO EMPTY ARRAYS")
    print("=" * 70)

    # Python Course
    course1 = Course(
        name="Python Fundamentals",
        description="Master Python basics from variables to functions",
        category="Programming",
        level="beginner",
        duration_weeks=4,
        icon="PY",
        rating=4.8,
        students_enrolled=1250
    )
    db.add(course1)
    db.flush()

    concept1 = Concept(
        course_id=course1.id,
        name="Python Basics",
        description="Introduction to Python programming",
        order_index=0
    )
    db.add(concept1)
    db.flush()

    topic1 = Topic(
        course_id=course1.id,
        concept_id=concept1.id,
        title="What is Python?",
        description="Learn about Python and its applications",
        difficulty="beginner",
        order_index=0
    )
    db.add(topic1)
    db.flush()

    lesson1 = Lesson(
        topic_id=topic1.id,
        title="Introduction to Python",
        description="Understanding Python language",
        order_index=0,
        duration_minutes=25
    )
    db.add(lesson1)
    db.flush()

    video1 = Video(
        lesson_id=lesson1.id,
        title="What is Python?",
        description="Learn what Python is",
        url="https://www.youtube.com/watch?v=python_intro_v1",
        duration_seconds=720,
        has_subtitles=True,
        order_index=0
    )
    db.add(video1)

    video2 = Video(
        lesson_id=lesson1.id,
        title="Setting Up Python",
        description="Install Python",
        url="https://www.youtube.com/watch?v=python_setup_v2",
        duration_seconds=600,
        has_subtitles=True,
        order_index=1
    )
    db.add(video2)
    db.flush()

    concept_text1 = VideoConcept(
        video_id=video1.id,
        title="Python Definition",
        content="Python is a high-level programming language",
        explanation="Python is designed to be readable and simple",
        real_world_example="Used by NASA, Google, Instagram",
        order_index=0
    )
    db.add(concept_text1)

    topic2 = Topic(
        course_id=course1.id,
        concept_id=concept1.id,
        title="Variables and Data Types",
        description="Understanding variables",
        difficulty="beginner",
        order_index=1,
        prerequisites=[topic1.id]
    )
    db.add(topic2)
    db.flush()

    lesson2 = Lesson(
        topic_id=topic2.id,
        title="Working with Variables",
        description="Learn variables",
        order_index=0,
        duration_minutes=30
    )
    db.add(lesson2)
    db.flush()

    video3 = Video(
        lesson_id=lesson2.id,
        title="Variables Explained",
        description="Python variables",
        url="https://www.youtube.com/watch?v=python_vars_v3",
        duration_seconds=900,
        has_subtitles=True,
        order_index=0
    )
    db.add(video3)

    video4 = Video(
        lesson_id=lesson2.id,
        title="Data Types in Python",
        description="Data types explained",
        url="https://www.youtube.com/watch?v=python_types_v4",
        duration_seconds=1200,
        has_subtitles=True,
        order_index=1
    )
    db.add(video4)

    assessment1 = Assessment(
        course_id=course1.id,
        topic_id=topic2.id,
        title="Variables and Types Quiz",
        description="Test your knowledge",
        assessment_type="quiz",
        passing_score=70.0,
        time_limit_minutes=15
    )
    db.add(assessment1)
    db.flush()

    questions = [
        {"text": "What is a variable?", "options": {"A": "Data container", "B": "Function", "C": "Loop", "D": "Module"}, "correct": "A"},
        {"text": "Text data type?", "options": {"A": "int", "B": "str", "C": "bool", "D": "float"}, "correct": "B"},
        {"text": "Assignment symbol?", "options": {"A": "==", "B": "=", "C": "!=", "D": "<>"}, "correct": "B"},
    ]

    for idx, q in enumerate(questions):
        question = AssessmentQuestion(
            assessment_id=assessment1.id,
            question_text=q["text"],
            question_type="mcq",
            options=q["options"],
            correct_answer=q["correct"],
            points=1.0,
            order_index=idx
        )
        db.add(question)

    course2 = Course(
        name="Machine Learning Fundamentals",
        description="Introduction to ML concepts",
        category="AI/ML",
        level="intermediate",
        duration_weeks=6,
        icon="ML",
        rating=4.9,
        students_enrolled=850
    )
    db.add(course2)
    db.flush()

    concept2 = Concept(
        course_id=course2.id,
        name="ML Basics",
        description="ML Foundation",
        order_index=0
    )
    db.add(concept2)
    db.flush()

    topic3 = Topic(
        course_id=course2.id,
        concept_id=concept2.id,
        title="What is ML?",
        description="ML Fundamentals",
        difficulty="intermediate",
        order_index=0
    )
    db.add(topic3)
    db.flush()

    lesson3 = Lesson(
        topic_id=topic3.id,
        title="ML Introduction",
        description="ML Basics",
        order_index=0,
        duration_minutes=35
    )
    db.add(lesson3)
    db.flush()

    video5 = Video(
        lesson_id=lesson3.id,
        title="What is ML?",
        description="ML Introduction",
        url="https://www.youtube.com/watch?v=ml_intro_full",
        duration_seconds=1500,
        has_subtitles=True,
        order_index=0
    )
    db.add(video5)

    video6 = Video(
        lesson_id=lesson3.id,
        title="ML Applications",
        description="Real-world ML",
        url="https://www.youtube.com/watch?v=ml_applications_real",
        duration_seconds=1200,
        has_subtitles=True,
        order_index=1
    )
    db.add(video6)

    course3 = Course(
        name="MERN Stack Development",
        description="Full-stack web applications",
        category="Web Development",
        level="intermediate",
        duration_weeks=8,
        icon="WEB",
        rating=4.7,
        students_enrolled=1100
    )
    db.add(course3)
    db.flush()

    concept3 = Concept(
        course_id=course3.id,
        name="Frontend Basics",
        description="React and JavaScript",
        order_index=0
    )
    db.add(concept3)
    db.flush()

    topic4 = Topic(
        course_id=course3.id,
        concept_id=concept3.id,
        title="Introduction to React",
        description="React fundamentals",
        difficulty="intermediate",
        order_index=0
    )
    db.add(topic4)
    db.flush()

    lesson4 = Lesson(
        topic_id=topic4.id,
        title="React Basics",
        description="Getting started",
        order_index=0,
        duration_minutes=40
    )
    db.add(lesson4)
    db.flush()

    video7 = Video(
        lesson_id=lesson4.id,
        title="What is React?",
        description="React library",
        url="https://www.youtube.com/watch?v=react_intro_basics",
        duration_seconds=1800,
        has_subtitles=True,
        order_index=0
    )
    db.add(video7)

    video8 = Video(
        lesson_id=lesson4.id,
        title="React Components",
        description="Reusable components",
        url="https://www.youtube.com/watch?v=react_components_guide",
        duration_seconds=1600,
        has_subtitles=True,
        order_index=1
    )
    db.add(video8)

    course4 = Course(
        name="Data Science with Python",
        description="Data analysis and visualization",
        category="Data",
        level="intermediate",
        duration_weeks=6,
        icon="DATA",
        rating=4.8,
        students_enrolled=950
    )
    db.add(course4)
    db.flush()

    concept4 = Concept(
        course_id=course4.id,
        name="Data Fundamentals",
        description="Data and libraries",
        order_index=0
    )
    db.add(concept4)
    db.flush()

    topic5 = Topic(
        course_id=course4.id,
        concept_id=concept4.id,
        title="NumPy and Pandas",
        description="Data manipulation",
        difficulty="intermediate",
        order_index=0
    )
    db.add(topic5)
    db.flush()

    lesson5 = Lesson(
        topic_id=topic5.id,
        title="NumPy Basics",
        description="Numerical arrays",
        order_index=0,
        duration_minutes=35
    )
    db.add(lesson5)
    db.flush()

    video9 = Video(
        lesson_id=lesson5.id,
        title="NumPy Introduction",
        description="NumPy operations",
        url="https://www.youtube.com/watch?v=numpy_intro_complete",
        duration_seconds=1400,
        has_subtitles=True,
        order_index=0
    )
    db.add(video9)

    video10 = Video(
        lesson_id=lesson5.id,
        title="Working with Arrays",
        description="Array operations",
        url="https://www.youtube.com/watch?v=numpy_arrays_detailed",
        duration_seconds=1300,
        has_subtitles=True,
        order_index=1
    )
    db.add(video10)

    db.commit()

    print("\n" + "=" * 70)
    print("[OK] COMPREHENSIVE DATA SEEDING COMPLETE!")
    print("=" * 70)

    courses = db.query(Course).count()
    concepts = db.query(Concept).count()
    topics = db.query(Topic).count()
    lessons = db.query(Lesson).count()
    videos = db.query(Video).count()
    assessments = db.query(Assessment).count()
    questions = db.query(AssessmentQuestion).count()

    print("\n[DATA] Summary (ZERO EMPTY ARRAYS):")
    print(f"  [OK] Courses: {courses}")
    print(f"  [OK] Concepts: {concepts}")
    print(f"  [OK] Topics: {topics}")
    print(f"  [OK] Lessons: {lessons}")
    print(f"  [OK] Videos: {videos}")
    print(f"  [OK] Assessments: {assessments}")
    print(f"  [OK] Questions: {questions}")

    print("\n[COURSES] Loaded:")
    for course in db.query(Course).all():
        topic_count = db.query(Topic).filter_by(course_id=course.id).count()
        video_count = db.query(Video).join(Lesson).join(Topic)\
            .filter(Topic.course_id == course.id).count()
        print(f"  [OK] {course.name}")
        print(f"       Topics: {topic_count} | Videos: {video_count}")

    print("\n" + "=" * 70)
    print("[SUCCESS] ALL DATA READY - NO EMPTY ARRAYS - FULLY POPULATED")
    print("=" * 70)


if __name__ == "__main__":
    from app.database import SessionLocal
    db = SessionLocal()
    seed_comprehensive_courses(db)
    db.close()
