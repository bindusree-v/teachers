#!/usr/bin/env python3
"""
Seed database with courses, topics, videos, and assessments
Run: python scripts/seed_db.py
"""

import sys
import os

# Fix Windows encoding issue with Unicode
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app import models
import json

def create_course_data():
    """Return course data structure"""
    return [
        {
            "name": "Python Fundamentals",
            "category": "Programming",
            "level": "beginner",
            "duration_weeks": 8,
            "description": "Learn Python basics, data types, control flow, and functions",
            "rating": 4.8,
            "icon": "🐍",
            "color": "#3776AB",
            "concepts": [
                {"name": "Python Basics", "topics": [
                    {"title": "Introduction & Setup", "lessons": [
                        {"title": "What is Python?", "videos": [
                            {"title": "Python Overview"}
                        ]}
                    ]},
                    {"title": "Variables & Data Types", "lessons": [
                        {"title": "Working with Strings, Numbers", "videos": [
                            {"title": "Data Types Explained"}
                        ]}
                    ]}
                ]},
                {"name": "Control Flow & Functions", "topics": [
                    {"title": "If-Else Statements", "lessons": [
                        {"title": "Conditional Logic", "videos": [
                            {"title": "If-Elif-Else Tutorial"}
                        ]}
                    ]},
                    {"title": "Functions & Loops", "lessons": [
                        {"title": "Writing Reusable Code", "videos": [
                            {"title": "Functions Deep Dive"}
                        ]}
                    ]}
                ]}
            ],
            "assessments": ["Python Basics Quiz", "Data Types Assessment"]
        },
        {
            "name": "MERN Stack Development",
            "category": "Web Development",
            "level": "intermediate",
            "duration_weeks": 12,
            "description": "Master MongoDB, Express, React, and Node.js",
            "rating": 4.9,
            "icon": "⚛️",
            "color": "#61DAFB",
            "concepts": [
                {"name": "React Fundamentals", "topics": [
                    {"title": "JSX & Components", "lessons": [
                        {"title": "Understanding JSX", "videos": [
                            {"title": "JSX Syntax"}
                        ]}
                    ]},
                    {"title": "Hooks & State Management", "lessons": [
                        {"title": "useState & useEffect", "videos": [
                            {"title": "useState Hook Deep Dive"}
                        ]}
                    ]}
                ]},
                {"name": "Backend with Node & Express", "topics": [
                    {"title": "REST APIs", "lessons": [
                        {"title": "Building API Endpoints", "videos": [
                            {"title": "Express Server Setup"}
                        ]}
                    ]},
                    {"title": "Database with MongoDB", "lessons": [
                        {"title": "CRUD Operations", "videos": [
                            {"title": "MongoDB Connection"}
                        ]}
                    ]}
                ]}
            ],
            "assessments": ["React Quiz", "Node.js Project"]
        },
        {
            "name": "Machine Learning Fundamentals",
            "category": "AI/ML",
            "level": "intermediate",
            "duration_weeks": 10,
            "description": "Supervised learning, unsupervised learning, and model evaluation",
            "rating": 4.7,
            "icon": "🤖",
            "color": "#FF6B6B",
            "concepts": [
                {"name": "Supervised Learning", "topics": [
                    {"title": "Linear Regression", "lessons": [
                        {"title": "Regression Basics", "videos": [
                            {"title": "Linear Regression Explained"}
                        ]},
                        {"title": "Cost Functions", "videos": [
                            {"title": "MSE, MAE, RMSE"}
                        ]}
                    ]},
                    {"title": "Classification", "lessons": [
                        {"title": "Logistic Regression", "videos": [
                            {"title": "Binary Classification"}
                        ]}
                    ]}
                ]},
                {"name": "Unsupervised Learning", "topics": [
                    {"title": "Clustering", "lessons": [
                        {"title": "K-Means Algorithm", "videos": [
                            {"title": "K-Means Tutorial"}
                        ]}
                    ]}
                ]}
            ],
            "assessments": ["ML Fundamentals Quiz", "Linear Regression Project"]
        },
        {
            "name": "Deep Learning & Neural Networks",
            "category": "AI/ML",
            "level": "advanced",
            "duration_weeks": 12,
            "description": "Neural networks, CNNs, RNNs, and transformers",
            "rating": 4.8,
            "icon": "🧠",
            "color": "#9945FF",
            "concepts": []
        },
        {
            "name": "Natural Language Processing",
            "category": "AI/ML",
            "level": "advanced",
            "duration_weeks": 10,
            "description": "Text processing, embeddings, and language models",
            "rating": 4.6,
            "icon": "📝",
            "color": "#00D9FF",
            "concepts": []
        },
        {
            "name": "Large Language Models (LLMs)",
            "category": "AI/ML",
            "level": "advanced",
            "duration_weeks": 8,
            "description": "Understanding and fine-tuning LLMs like GPT",
            "rating": 4.9,
            "icon": "💬",
            "color": "#00C9A7",
            "concepts": []
        },
        {
            "name": "Prompt Engineering & LLM Applications",
            "category": "AI/ML",
            "level": "intermediate",
            "duration_weeks": 6,
            "description": "Advanced prompting techniques and LLM integration",
            "rating": 4.7,
            "icon": "⚡",
            "color": "#FFB627",
            "concepts": []
        },
        {
            "name": "Retrieval-Augmented Generation (RAG)",
            "category": "AI/ML",
            "level": "advanced",
            "duration_weeks": 8,
            "description": "Building RAG systems with embeddings and LLMs",
            "rating": 4.8,
            "icon": "🔍",
            "color": "#FF006E",
            "concepts": []
        },
        {
            "name": "Generative AI & Image Generation",
            "category": "AI/ML",
            "level": "advanced",
            "duration_weeks": 8,
            "description": "Diffusion models, GANs, and DALL-E, Stable Diffusion",
            "rating": 4.7,
            "icon": "🎨",
            "color": "#FB5607",
            "concepts": []
        },
        {
            "name": "Computer Vision & Image Processing",
            "category": "AI/ML",
            "level": "advanced",
            "duration_weeks": 10,
            "description": "Image classification, object detection, segmentation",
            "rating": 4.8,
            "icon": "👁️",
            "color": "#3A86FF",
            "concepts": []
        },
    ]

def seed_database():
    """Populate database with initial data"""

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

    db = SessionLocal()

    try:
        # Check if courses already exist
        existing_courses = db.query(models.Course).count()
        if existing_courses > 0:
            print(f"ℹ️  Database already has {existing_courses} courses. Skipping seed.")
            return

        courses_data = create_course_data()

        for course_data in courses_data:
            # Create course
            course = models.Course(
                name=course_data["name"],
                category=course_data["category"],
                level=course_data["level"],
                duration_weeks=course_data["duration_weeks"],
                description=course_data["description"],
                rating=course_data["rating"],
                icon=course_data["icon"],
                color=course_data["color"]
            )
            db.add(course)
            db.flush()

            # Add concepts and topics
            concept_index = 0
            for concept_data in course_data.get("concepts", []):
                concept = models.Concept(
                    course_id=course.id,
                    name=concept_data["name"],
                    order_index=concept_index
                )
                db.add(concept)
                db.flush()

                topic_index = 0
                for topic_data in concept_data.get("topics", []):
                    topic = models.Topic(
                        course_id=course.id,
                        concept_id=concept.id,
                        title=topic_data["title"],
                        difficulty=topic_data.get("difficulty", "beginner"),
                        order_index=topic_index
                    )
                    db.add(topic)
                    db.flush()

                    lesson_index = 0
                    for lesson_data in topic_data.get("lessons", []):
                        lesson = models.Lesson(
                            topic_id=topic.id,
                            title=lesson_data["title"],
                            order_index=lesson_index
                        )
                        db.add(lesson)
                        db.flush()

                        video_index = 0
                        for video_data in lesson_data.get("videos", []):
                            video = models.Video(
                                lesson_id=lesson.id,
                                title=video_data["title"],
                                url=f"/videos/{course.id}/{topic.id}/{video_index}.mp4",
                                duration_seconds=3600,
                                has_subtitles=True,
                                order_index=video_index
                            )
                            db.add(video)
                            db.flush()

                            # Add video concepts
                            video_concept = models.VideoConcept(
                                video_id=video.id,
                                title=video_data["title"],
                                content=f"Explanation of {video_data['title']}",
                                order_index=0
                            )
                            db.add(video_concept)

                            # Add subtitles
                            for lang in ["en", "hi", "es"]:
                                subtitle = models.Subtitle(
                                    video_id=video.id,
                                    language=lang,
                                    content=f"Subtitles for {video_data['title']} in {lang}"
                                )
                                db.add(subtitle)

                            video_index += 1

                        lesson_index += 1

                    topic_index += 1

                concept_index += 1

            # Add assessments
            for assessment_name in course_data.get("assessments", []):
                assessment = models.Assessment(
                    course_id=course.id,
                    title=assessment_name,
                    passing_score=60.0
                )
                db.add(assessment)
                db.flush()

                # Add questions
                for i in range(5):
                    question = models.AssessmentQuestion(
                        assessment_id=assessment.id,
                        question_text=f"Question {i+1} for {assessment_name}",
                        question_type="mcq",
                        options={
                            "A": "Option A",
                            "B": "Option B",
                            "C": "Option C",
                            "D": "Option D",
                            "correct": "C"
                        },
                        correct_answer="C",
                        points=1.0
                    )
                    db.add(question)

            print(f"✅ Created course: {course.name}")

        # Commit all changes
        db.commit()
        print(f"\n🎉 Successfully seeded database with {len(courses_data)} courses!")
        print(f"📊 Total data points:")
        print(f"   - Courses: {db.query(models.Course).count()}")
        print(f"   - Concepts: {db.query(models.Concept).count()}")
        print(f"   - Topics: {db.query(models.Topic).count()}")
        print(f"   - Lessons: {db.query(models.Lesson).count()}")
        print(f"   - Videos: {db.query(models.Video).count()}")
        print(f"   - Assessments: {db.query(models.Assessment).count()}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
