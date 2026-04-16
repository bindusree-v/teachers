from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel
from datetime import datetime
import os
import shutil
from pathlib import Path
import random
import json
import re
from PyPDF2 import PdfReader

router = APIRouter(prefix="/api/v1/assessments", tags=["assessments"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/assessments")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class SubmitAssessmentRequest(BaseModel):
    student_id: int
    answers: dict

class CreateAssessmentRequest(BaseModel):
    title: str
    description: str
    course_id: int
    topic_id: int
    assessment_type: str = "quiz"
    passing_score: int = 70
    time_limit_minutes: int = 30
    questions: list

class CreateQuestionRequest(BaseModel):
    question_text: str
    question_type: str  # "mcq" or "text"
    options: dict = None  # For MCQ: {"A": "option1", "B": "option2", "correct": "A"}
    points: int = 1

@router.get("/{assessment_id}")
def get_assessment(assessment_id: int, student_id: int = None, db: Session = Depends(get_db)):
    """Get assessment with questions (randomized for each student)"""
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    questions = db.query(models.AssessmentQuestion).filter(
        models.AssessmentQuestion.assessment_id == assessment_id
    ).all()

    # Randomize questions for each student to prevent cheating
    if student_id:
        random.seed(student_id + assessment_id)  # Deterministic randomization per student
        questions = random.sample(questions, len(questions))

    return {
        "assessment": {
            "id": assessment.id,
            "title": assessment.title,
            "description": assessment.description,
            "assessment_type": assessment.assessment_type,
            "passing_score": assessment.passing_score,
            "time_limit_minutes": assessment.time_limit_minutes
        },
        "questions": [{
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": q.options if q.question_type == "mcq" else None,
            "points": q.points
        } for q in questions]
    }

@router.post("/{assessment_id}/submit")
def submit_assessment(
    assessment_id: int,
    request: SubmitAssessmentRequest,
    db: Session = Depends(get_db)
):
    """Submit assessment and calculate score"""
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    questions = db.query(models.AssessmentQuestion).filter(
        models.AssessmentQuestion.assessment_id == assessment_id
    ).all()

    if not questions:
        raise HTTPException(status_code=400, detail="No questions in assessment")

    # Calculate score
    correct_count = 0
    total_points = 0

    for question in questions:
        total_points += question.points
        q_id = str(question.id)

        if q_id in request.answers:
            answer = request.answers[q_id]

            # Check if correct
            if question.question_type == "mcq":
                if answer.get("selected_option") == question.options.get("correct"):
                    correct_count += question.points

    # Calculate percentage
    score_percentage = (correct_count / total_points * 100) if total_points > 0 else 0
    is_passed = score_percentage >= assessment.passing_score

    # Store result
    result = models.AssessmentResult(
        student_id=request.student_id,
        assessment_id=assessment_id,
        score=int(score_percentage),
        passing_score=assessment.passing_score,
        is_passed=is_passed,
        answers=request.answers,
        time_taken_seconds=0
    )

    db.add(result)

    # Update topic progress if topic exists
    if assessment.topic_id:
        topic_prog = db.query(models.TopicProgress).filter(
            models.TopicProgress.student_id == request.student_id,
            models.TopicProgress.topic_id == assessment.topic_id
        ).first()

        if not topic_prog:
            topic_prog = models.TopicProgress(
                student_id=request.student_id,
                topic_id=assessment.topic_id,
                status="in_progress",
                mastery_level=0.0
            )
            db.add(topic_prog)

        # Update mastery level
        if is_passed:
            topic_prog.mastery_level = min(topic_prog.mastery_level + 0.2, 1.0)
            if topic_prog.mastery_level >= 0.6:
                topic_prog.status = "completed"

    db.commit()

    return {
        "score": int(score_percentage),
        "is_passed": is_passed,
        "passing_score": assessment.passing_score,
        "feedback": f"Score: {int(score_percentage)}%. {'✓ Passed!' if is_passed else '✗ Need more practice'}"
    }

@router.get("/topic/{topic_id}")
def get_topic_assessments(topic_id: int, db: Session = Depends(get_db)):
    """Get assessments for a topic"""
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    assessments = db.query(models.Assessment).filter(models.Assessment.topic_id == topic_id).all()

    return {
        "topic": {
            "id": topic.id,
            "title": topic.title
        },
        "assessments": [{
            "id": a.id,
            "title": a.title,
            "assessment_type": a.assessment_type,
            "passing_score": a.passing_score
        } for a in assessments]
    }

@router.get("/student/{student_id}/results")
def get_student_results(student_id: int, db: Session = Depends(get_db)):
    """Get all assessment results for a student"""
    results = db.query(models.AssessmentResult).filter(
        models.AssessmentResult.student_id == student_id
    ).all()

    return {
        "student_id": student_id,
        "total_assessments": len(results),
        "results": [{
            "id": r.id,
            "assessment_id": r.assessment_id,
            "score": r.score,
            "is_passed": r.is_passed,
            "submission_date": r.submission_date
        } for r in results]
    }

@router.post("/create")
def create_assessment(request: CreateAssessmentRequest, db: Session = Depends(get_db)):
    """Create a new assessment for a topic"""
    # Check if topic exists
    topic = db.query(models.Topic).filter(models.Topic.id == request.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Create assessment
    assessment = models.Assessment(
        title=request.title,
        description=request.description,
        topic_id=request.topic_id,
        assessment_type=request.assessment_type,
        passing_score=request.passing_score,
        time_limit_minutes=request.time_limit_minutes
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Create questions
    for q_data in request.questions:
        question = models.AssessmentQuestion(
            assessment_id=assessment.id,
            question_text=q_data["question_text"],
            question_type=q_data["question_type"],
            options=q_data.get("options"),
            points=q_data.get("points", 1)
        )
        db.add(question)

    db.commit()

    return {
        "success": True,
        "assessment": {
            "id": assessment.id,
            "title": assessment.title,
            "description": assessment.description,
            "topic_id": assessment.topic_id,
            "assessment_type": assessment.assessment_type,
            "passing_score": assessment.passing_score,
            "time_limit_minutes": assessment.time_limit_minutes,
            "questions_count": len(request.questions)
        }
    }

@router.post("/create-from-pdf")
async def create_assessment_from_pdf(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    course_id: int = Form(...),
    topic_id: int = Form(...),
    assessment_type: str = Form("quiz"),
    passing_score: int = Form(70),
    time_limit_minutes: int = Form(30),
    db: Session = Depends(get_db)
):
    """Create assessment from PDF upload with random question selection"""
    # Validate file type
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")

    # Check if topic exists
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Save PDF file
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{title.replace(' ', '_')}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Parse PDF to extract questions
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")

    # Parse questions from text
    # Expected format:
    # Question 1: What is 2+2?
    # A) 3
    # B) 4
    # C) 5
    # D) 6
    # Correct: B
    questions = []
    question_pattern = r'Question \d+:\s*(.*?)(?=Question \d+:|$)'
    option_pattern = r'([A-D])\)\s*(.*?)(?=[A-D]\)|Correct:|$)'
    correct_pattern = r'Correct:\s*([A-D])'

    question_matches = re.findall(question_pattern, text, re.DOTALL | re.IGNORECASE)

    for i, question_text in enumerate(question_matches):
        question_text = question_text.strip()
        if not question_text:
            continue

        # Find options for this question
        start_pos = text.find(f"Question {i+1}:")
        if start_pos == -1:
            continue

        next_question_pos = text.find(f"Question {i+2}:", start_pos)
        if next_question_pos == -1:
            next_question_pos = len(text)

        question_block = text[start_pos:next_question_pos]

        # Extract options
        options = {}
        option_matches = re.findall(option_pattern, question_block, re.IGNORECASE)
        for letter, option_text in option_matches:
            options[letter.upper()] = option_text.strip()

        # Extract correct answer
        correct_match = re.search(correct_pattern, question_block, re.IGNORECASE)
        correct_answer = correct_match.group(1).upper() if correct_match else None

        if options and correct_answer and correct_answer in options:
            questions.append({
                "question_text": question_text,
                "question_type": "mcq",
                "options": {**options, "correct": correct_answer},
                "points": 1
            })

    if not questions:
        raise HTTPException(status_code=400, detail="No valid questions found in PDF. Please ensure questions are formatted as: Question 1: [text] A) [option] B) [option] C) [option] D) [option] Correct: [A-D]")

    # Create assessment
    assessment = models.Assessment(
        title=title,
        description=description,
        course_id=course_id,
        topic_id=topic_id,
        assessment_type=assessment_type,
        passing_score=passing_score,
        time_limit_minutes=time_limit_minutes
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # Create questions
    for q_data in questions:
        question = models.AssessmentQuestion(
            assessment_id=assessment.id,
            question_text=q_data["question_text"],
            question_type=q_data["question_type"],
            options=q_data.get("options"),
            points=q_data.get("points", 1)
        )
        db.add(question)

    db.commit()

    return {
        "success": True,
        "assessment": {
            "id": assessment.id,
            "title": assessment.title,
            "description": assessment.description,
            "course_id": assessment.course_id,
            "topic_id": assessment.topic_id,
            "assessment_type": assessment.assessment_type,
            "passing_score": assessment.passing_score,
            "time_limit_minutes": assessment.time_limit_minutes,
            "questions_count": len(questions),
            "pdf_path": str(file_path)
        }
    }
