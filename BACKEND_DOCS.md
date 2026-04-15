# Adaptive Learning Engine - Backend Documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Start Backend Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

---

## 📋 Architecture Overview

### Core Components

1. **Data Models** (`models.py`)
   - Student: Core student information
   - KnowledgeState: Structured knowledge representation
   - PerformanceData: Continuous data ingestion
   - Recommendation: AI-driven topic recommendations
   - PathVersion: Historical learning path decisions
   - TeacherOverride: Teacher interventions
   - DifficultyLog: Calibration history

2. **Services** (`services.py`)
   - RecommendationEngine: Generates next best learning action
   - DifficultyCalibration: Dynamically adjusts content complexity
   - DataIngestionPipeline: Ingests assessment, attendance, engagement, doubt data
   - TeacherFeedbackLoop: Processes teacher overrides
   - PathVersioning: Maintains learning path history

3. **API Endpoints** (`main.py`)
   - Student endpoints: Dashboard, analytics, recommendations
   - Teacher endpoints: Dashboard, overrides, effectiveness rating
   - Data ingestion: Assessment, attendance, engagement, doubt data
   - Admin endpoints: Database management

---

## 📡 API Endpoints

### Student Endpoints

#### Get Student Dashboard
```
GET /student/{student_id}
```
Returns comprehensive student dashboard with current progress, recommendations, and learning path.

**Response Example:**
```json
{
  "student_name": "Rahul",
  "mastery": 0.62,
  "current_topic": "Control Statements",
  "completed_topics": 2,
  "assessments_taken": 3,
  "strong_area": "Variables and Data Types",
  "weak_area": "Logic Building",
  "learning_path": ["Introduction to Python", "Variables and Data Types", "Control Statements"],
  "recommendation": {
    "topic": "Control Statements",
    "difficulty": "medium",
    "reasons": ["..."
    ],
    "skill_area": "Logic Building",
    "confidence_score": 0.85
  }
}
```

#### Get Student Analytics
```
GET /student/{student_id}/analytics
```
Detailed performance analytics with history and trends.

#### Get Student Knowledge State
```
GET /student/{student_id}/knowledge-state
```
Returns structured knowledge representation: which topics student knows and mastery levels.

#### Get Recommendation
```
GET /student/{student_id}/recommendation
```
AI-generated recommendation for next best learning topic using the Recommendation Engine.

#### Get Path History
```
GET /student/{student_id}/path-history?limit=20
```
Historical path decisions for audit trails and model improvement.

---

### Teacher Endpoints

#### Get Teacher Dashboard
```
GET /teacher/dashboard
```
Overview of all students, their status, progress, and weak areas.

#### Teacher Override
```
POST /teacher/override
```
Override AI recommendation and redirect student to different topic.

**Request:**
```json
{
  "student_id": 1,
  "original_recommendation": "Control Statements",
  "override_to_topic": "Functions",
  "override_to_difficulty": "hard",
  "reason": "Student showed advanced understanding",
  "teacher_notes": "Demonstrated strong grasp of logic"
}
```

#### Rate Override Effectiveness
```
POST /teacher/rate-override?override_id=1&effectiveness=0.9
```
Teacher provides feedback on how effective an override was.

---

### Data Ingestion Endpoints

All endpoints for ingesting continuous data from platform modules:

#### Ingest Assessment Data
```
POST /data/assessment
```
Student assessment scores, quiz results, exam performance.

**Request:**
```json
{
  "student_id": 1,
  "topic": "Control Statements",
  "score": 85.5,
  "assessment_type": "quiz"
}
```

#### Ingest Attendance Data
```
POST /data/attendance
```

#### Ingest Engagement Data
```
POST /data/engagement
```
Interaction count, time spent, resource type accessed.

#### Ingest Doubt Data
```
POST /data/doubt
```
Questions asked and resolved.

#### Batch Update
```
POST /data/batch-update
```
Update multiple data types simultaneously for a student.

---

## 🤖 Recommendation Engine

The recommendation engine determines the next best learning action for each student using:

1. **Mastery Scores**: Calculated from completed topics and recent assessments
2. **Learning Path**: Current position in curriculum
3. **Performance Metrics**: Assessment scores, time spent, engagement
4. **Knowledge Gaps**: Weak areas vs strong areas
5. **Learning Pace**: Individual student learning speed

### Algorithm
- Checks if student has mastered current topic (60% threshold)
- If yes, progresses to next topic
- If no, recommends practice on current topic
- Adjusts difficulty based on performance

### Output
```json
{
  "topic": "Next recommended topic",
  "difficulty": "easy|medium|hard",
  "reasons": ["Why this recommendation"],
  "skill_area": "Area of improvement",
  "confidence_score": 0.85
}
```

---

## ⚙️ Difficulty Calibration

Automatically adjusts content difficulty based on:

- **Assessment Scores**: >85% = increase, <40% = decrease
- **Time on Topic**: Too fast with high score = increase difficulty
- **Engagement**: Low interaction = decrease difficulty
- **Struggle Indicators**: Multiple failed attempts = decrease

### Calibration Triggers

| Condition | Action |
|-----------|--------|
| Score >85, Time <30min | Increase difficulty |
| Score <40 | Decrease difficulty |
| Low engagement | Decrease difficulty |
| Struggling >1 hour | Decrease difficulty |

---

## 📊 Knowledge State Model

Maintains structured, always-updated representation of what each student knows:

```json
{
  "student_id": 1,
  "knowledge_map": {
    "Introduction to Python": 0.95,
    "Variables and Data Types": 0.85,
    "Control Statements": 0.60,
    "Functions": 0.0
  },
  "skill_profile": {
    "Basics": 0.90,
    "Logic Building": 0.60,
    "Modularity": 0.0
  },
  "learning_pace": 1.2,
  "optimal_difficulty": "medium",
  "last_updated": "2024-04-14T20:30:00"
}
```

---

## 🔄 Data Ingestion Pipeline

### Continuous Data Sources

1. **Assessments**
   - Quiz scores
   - Exam performance
   - Coding challenge results
   - Assessment type

2. **Attendance**
   - Session presence
   - Session duration
   - Login status

3. **Engagement**
   - Resource interactions
   - Time on topic
   - Resource type (video, article, interactive)

4. **Doubts/Questions**
   - Questions asked
   - Questions resolved
   - Question difficulty level

All data flows into the PerformanceData model for analysis.

---

## 👨‍🏫 Teacher Feedback Loop

### Override Process

1. Teacher views student dashboard
2. Reviews AI recommendation
3. Chooses to override if needed
4. Provides reason for override
5. System records decision
6. Model learns from override
7. Teacher can rate effectiveness

### Model Learning

Overrides feed back as:
- PathVersion records
- TeacherOverride entries with reasoning
- Effectiveness ratings for improvement

---

## 📈 Path Versioning

Complete audit trail of student's learning path:

```json
{
  "version": 1,
  "from_topic": "Variables and Data Types",
  "to_topic": "Control Statements",
  "difficulty": "medium",
  "timestamp": "2024-04-14T20:00:00",
  "was_optimal": true,
  "performance_change": 0.05
}
```

### Use Cases

- **Audit Trail**: Complete learning path history
- **Model Improvement**: Analyze optimal vs suboptimal paths
- **Student Analysis**: Understand learning progression
- **Performance Prediction**: What paths lead to success?

---

## 🗄️ Database Schema

### Tables

- **students**: Core student info
- **knowledge_state**: Structured knowledge representation
- **performance_data**: All ingested performance metrics
- **recommendations**: Active recommendations with reasoning
- **topic_progress**: Progress on each topic
- **path_versions**: Learning path history
- **teacher_overrides**: Teacher interventions
- **difficulty_logs**: Difficulty calibration history

---

## 🔧 Configuration

### Database
- SQLite by default (lightweight, development)
- Stored at: `adaptive_learning.db`
- Can be switched to PostgreSQL/MySQL in production

### API Port
- Development: `8000`

### CORS
- Allows: `localhost:5173` (frontend dev server)
- Can be configured in main.py

---

## 🧪 Testing

### Health Check
```
curl http://localhost:8000/health
```

### Get All Students
```
curl http://localhost:8000/students
```

### Get Specific Student
```
curl http://localhost:8000/student/1
```

### Get API Documentation
Visit: `http://localhost:8000/docs`

---

## 📝 Sample Workflow

### 1. Student Takes Assessment
```
POST/data/assessment
{
  "student_id": 1,
  "topic": "Control Statements",
  "score": 82,
  "assessment_type": "quiz"
}
```

### 2. Get Recommendation
```
GET /student/1/recommendation
```

### 3. System Calibrates Difficulty
```
POST /student/1/calibrate-difficulty/Control%20Statements
```

### 4. Teacher Views Dashboard
```
GET /teacher/dashboard
```

### 5. Teacher Overrides if Needed
```
POST /teacher/override
{
  "student_id": 1,
  "original_recommendation": "Control Statements",
  "override_to_topic": "Functions",
  "override_to_difficulty": "hard",
  "reason": "Student demonstrated mastery"
}
```

---

## 🚀 Production Considerations

1. **Database**: Migrate to PostgreSQL for scalability
2. **Authentication**: Add JWT token-based auth
3. **Logging**: Implement structured logging
4. **Caching**: Add Redis for performance
5. **Rate Limiting**: Protect API endpoints
6. **Monitoring**: Add health checks and metrics
7. **Testing**: Comprehensive test suite
8. **Documentation**: API documentation (Swagger UI active at /docs)

---

## 📞 Support

For issues or questions:
- Check API documentation at `/docs`
- Review error responses for guidance
- Ensure frontend and backend are both running
- Verify database is initialized with seed data

---

## 📄 License

MIT
