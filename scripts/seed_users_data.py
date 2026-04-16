#!/usr/bin/env python3
"""
Seed database with 20 users: 15 Students + 5 Teachers
Run: python scripts/seed_users_data.py
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
from datetime import datetime, timedelta
import random

def seed_users():
    """Seed 15 students and 5 teachers with realistic data"""

    db = SessionLocal()

    try:
        print("\n" + "="*60)
        print("SEEDING 20 USERS (15 STUDENTS + 5 TEACHERS)")
        print("="*60 + "\n")

        # ==================== CREATE STUDENTS ====================
        students_data = [
            {"name": "Rahul Kumar", "email": "rahul.kumar@student.com", "topic": "Variables and Data Types", "strong": "Python", "weak": "OOP", "mastery": 0.62},
            {"name": "Anjali Singh", "email": "anjali.singh@student.com", "topic": "Functions", "strong": "Functions", "weak": "Modules", "mastery": 0.78},
            {"name": "Kiran Patel", "email": "kiran.patel@student.com", "topic": "Control Statements", "strong": "Loops", "weak": "Recursion", "mastery": 0.45},
            {"name": "Priya Sharma", "email": "priya.sharma@student.com", "topic": "Loops", "strong": "Data Structures", "weak": "Algorithms", "mastery": 0.71},
            {"name": "Amit Desai", "email": "amit.desai@student.com", "topic": "Dictionaries", "strong": "Problem Solving", "weak": "Classes", "mastery": 0.68},
            {"name": "Neha Reddy", "email": "neha.reddy@student.com", "topic": "Lists", "strong": "Arrays", "weak": "Sorting", "mastery": 0.55},
            {"name": "Vikas Gupta", "email": "vikas.gupta@student.com", "topic": "String Manipulation", "strong": "Strings", "weak": "Regex", "mastery": 0.72},
            {"name": "Zara Khan", "email": "zara.khan@student.com", "topic": "File Handling", "strong": "I/O", "weak": "Error Handling", "mastery": 0.63},
            {"name": "Rohan Bhat", "email": "rohan.bhat@student.com", "topic": "Exception Handling", "strong": "Debugging", "weak": "Testing", "mastery": 0.58},
            {"name": "Isha Verma", "email": "isha.verma@student.com", "topic": "OOP Basics", "strong": "Inheritance", "weak": "Polymorphism", "mastery": 0.70},
            {"name": "Arjun Nair", "email": "arjun.nair@student.com", "topic": "Classes and Objects", "strong": "Encapsulation", "weak": "Abstraction", "mastery": 0.66},
            {"name": "Divya Chatterjee", "email": "divya.chatterjee@student.com", "topic": "Modules", "strong": "Imports", "weak": "Packages", "mastery": 0.51},
            {"name": "Sanjay Iyer", "email": "sanjay.iyer@student.com", "topic": "Decorators", "strong": "Functional Programming", "weak": "Meta-programming", "mastery": 0.73},
            {"name": "Meera Joshi", "email": "meera.joshi@student.com", "topic": "Database", "strong": "SQL", "weak": "NoSQL", "mastery": 0.64},
            {"name": "Arun Krishnan", "email": "arun.krishnan@student.com", "topic": "Web Development", "strong": "Backend", "weak": "Frontend", "mastery": 0.59},
        ]

        print("Adding 15 STUDENTS:")
        print("-" * 60)

        for i, data in enumerate(students_data, 1):
            # Check if student already exists
            existing = db.query(models.Student).filter(models.Student.email == data["email"]).first()
            if not existing:
                student = models.Student(
                    name=data["name"],
                    email=data["email"],
                    current_topic=data["topic"],
                    completed_topics=random.randint(3, 8),
                    assessments_taken=random.randint(2, 10),
                    strong_area=data["strong"],
                    weak_area=data["weak"],
                    mastery=data["mastery"],
                    is_logged_in=random.choice([True, False]),
                    is_active=True
                )
                db.add(student)
                print(f"  {i:2d}. {data['name']:25s} - {data['topic']:25s} (Mastery: {data['mastery']*100:.0f}%)")
            else:
                print(f"  {i:2d}. {data['name']:25s} - Already exists")

        db.commit()
        print("\n✅ 15 Students added successfully!\n")

        # ==================== CREATE TEACHERS ====================
        teachers_data = [
            {"name": "Dr. Rajesh Kumar", "email": "rajesh.kumar@teacher.com", "subject": "Python Programming", "exp": 8, "qual": "PhD", "areas": ["Python", "OOP", "Data Structures"]},
            {"name": "Prof. Aisha Hassan", "email": "aisha.hassan@teacher.com", "subject": "Web Development", "exp": 6, "qual": "M.Tech", "areas": ["React", "JavaScript", "HTML/CSS"]},
            {"name": "Dr. Chen Wei", "email": "chen.wei@teacher.com", "subject": "Machine Learning", "exp": 10, "qual": "PhD", "areas": ["ML", "Neural Networks", "Data Science"]},
            {"name": "Mr. James Smith", "email": "james.smith@teacher.com", "subject": "Database Systems", "exp": 7, "qual": "M.Sc", "areas": ["SQL", "MongoDB", "Database Design"]},
            {"name": "Ms. Maria Garcia", "email": "maria.garcia@teacher.com", "subject": "AI and Automation", "exp": 5, "qual": "Masters", "areas": ["AI", "LLMs", "Automation"]},
        ]

        print("Adding 5 TEACHERS:")
        print("-" * 60)

        for i, data in enumerate(teachers_data, 1):
            # Check if teacher already exists
            existing = db.query(models.Teacher).filter(models.Teacher.email == data["email"]).first()
            if not existing:
                teacher = models.Teacher(
                    name=data["name"],
                    email=data["email"],
                    subject=data["subject"],
                    expertise_areas=data["areas"],
                    courses_taught=random.randint(2, 5),
                    students_managed=random.randint(20, 60),
                    experience_years=data["exp"],
                    qualification=data["qual"],
                    phone=f"+91-{random.randint(7000000000, 9999999999)}",
                    is_active=True
                )
                db.add(teacher)
                print(f"  {i}. {data['name']:25s} - {data['subject']:25s} ({data['exp']} yrs)")
            else:
                print(f"  {i}. {data['name']:25s} - Already exists")

        db.commit()
        print("\n✅ 5 Teachers added successfully!\n")

        # ==================== ADD PERFORMANCE DATA ====================
        print("Adding PERFORMANCE DATA for Students:")
        print("-" * 60)

        students = db.query(models.Student).all()
        topics = ["Python Basics", "Functions", "Loops", "Data Structures", "OOP"]

        for student in students:
            for j in range(random.randint(3, 8)):
                perf = models.PerformanceData(
                    student_id=student.id,
                    assessment_score=random.uniform(40, 100),
                    assessment_type=random.choice(["quiz", "exam", "coding_challenge"]),
                    attendance_status=random.choice(["present", "absent", "excused"]),
                    session_duration=random.uniform(30, 180),
                    interaction_count=random.randint(10, 50),
                    time_on_topic=random.uniform(20, 120),
                    resource_type=random.choice(["video", "article", "interactive"]),
                    topic_name=random.choice(topics),
                    doubts_asked=random.randint(0, 5),
                    doubts_resolved=random.randint(0, 5),
                    question_difficulty=random.choice(["easy", "medium", "hard"]),
                    timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                db.add(perf)

        db.commit()
        print(f"  ✓ Performance records added for {len(students)} students")

        # ==================== SUMMARY ====================
        print("\n" + "="*60)
        print("SEEDING COMPLETE!")
        print("="*60)

        # Count totals
        total_students = db.query(models.Student).count()
        total_teachers = db.query(models.Teacher).count()
        total_performance = db.query(models.PerformanceData).count()

        print(f"\n📊 DATABASE SUMMARY:")
        print(f"   Total Students:        {total_students}")
        print(f"   Total Teachers:        {total_teachers}")
        print(f"   Performance Records:   {total_performance}")
        print(f"   Courses Available:     {db.query(models.Course).count()}")
        print(f"   Videos:                {db.query(models.Video).count()}")
        print(f"   Assessments:           {db.query(models.Assessment).count()}")
        print("\n✅ All data successfully seeded!\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        db.rollback()
        return False
    finally:
        db.close()

    return True

if __name__ == "__main__":
    success = seed_users()
    sys.exit(0 if success else 1)
