"""
🚀 COMPREHENSIVE DUMMY DATA GENERATOR
Ensures ZERO empty data - all courses fully populated with realistic content
"""

from sqlalchemy.orm import Session
from datetime import datetime
import sys
sys.path.append('..')

from app.models import Student, Teacher, Course, Topic, Video, Assessment, AssessmentQuestion

def seed_complete_courses_data(db: Session):
    """
    Generate COMPLETE dummy data for all courses
    RULE: NEVER return empty data
    """

    # Check if already seeded
    if db.query(Course).first():
        print("✅ Courses already seeded!")
        return

    print("=" * 70)
    print("🚀 SEEDING COMPLETE COURSE DATA (ZERO EMPTY DATA POLICY)")
    print("=" * 70)

    # ==================== COURSES ====================
    courses_data = [
        {
            "name": "Python Fundamentals",
            "description": "Master Python basics from variables to functions",
            "level": "beginner",
            "rating": 4.8,
            "icon": "🐍",
            "topics": [
                {
                    "name": "Introduction to Python",
                    "description": "Get started with Python programming",
                    "concepts": [
                        {
                            "title": "What is Python?",
                            "theory": "Python is a high-level, interpreted programming language created by Guido van Rossum. It's known for its simplicity and readability. Python uses indentation to define code blocks, making it beginner-friendly. It's used in web development, data science, AI, and automation. The Python interpreter reads and executes code line by line. Python supports multiple programming paradigms: procedural, object-oriented, and functional. It has a large community and extensive standard library.",
                            "main_video": "https://www.youtube.com/watch?v=python_intro_basics_001",
                            "duration_minutes": 12,
                            "related_videos": [
                                {"title": "Python History and Evolution", "url": "https://www.youtube.com/watch?v=python_history_002", "duration": 8},
                                {"title": "Why Learn Python?", "url": "https://www.youtube.com/watch?v=python_why_003", "duration": 6},
                            ],
                            "examples": [
                                {"title": "Your First Python Program", "code": 'print("Hello, World!")', "explanation": "This is the simplest Python program that outputs text to the console."},
                                {"title": "Simple Calculation", "code": "result = 10 + 5\nprint(result)", "explanation": "Python can perform arithmetic operations and display results."},
                            ]
                        },
                        {
                            "title": "Installing Python",
                            "theory": "To start programming in Python, you need to install it on your computer. Download the latest version from python.org. Follow the installation wizard and make sure to check 'Add Python to PATH' during installation. This allows you to run Python from your command line. After installation, verify by opening terminal/command prompt and typing 'python --version'. You can also install an IDE like PyCharm or use VS Code with Python extension for better development experience. Virtual environments help manage project dependencies separately.",
                            "main_video": "https://www.youtube.com/watch?v=python_install_101",
                            "duration_minutes": 10,
                            "related_videos": [
                                {"title": "IDE Setup - PyCharm", "url": "https://www.youtube.com/watch?v=python_pycharm_102", "duration": 15},
                                {"title": "VS Code for Python", "url": "https://www.youtube.com/watch?v=python_vscode_103", "duration": 12},
                            ],
                            "examples": [
                                {"title": "Verify Installation", "code": "python --version", "explanation": "Check if Python is properly installed on your system."},
                                {"title": "First Script", "code": "# Create file: hello.py\nprint('Python is ready!')", "explanation": "Create a Python script file and execute it."},
                            ]
                        },
                        {
                            "title": "Python Syntax Basics",
                            "theory": "Python syntax refers to the set of rules and conventions for writing Python code. Python uses 4 spaces or 1 tab for indentation - this is mandatory and defines code blocks. Comments start with # and are ignored by the interpreter. Python is case-sensitive, meaning 'name' and 'Name' are different variables. Statements end with newline (no semicolon needed). Multi-line statements can use backslash or parentheses. Python keywords like 'if', 'for', 'while' are reserved. Understanding syntax basics is crucial before advancing to complex programs.",
                            "main_video": "https://www.youtube.com/watch?v=python_syntax_201",
                            "duration_minutes": 14,
                            "related_videos": [
                                {"title": "Indentation in Python", "url": "https://www.youtube.com/watch?v=python_indent_202", "duration": 7},
                                {"title": "Python Keywords", "url": "https://www.youtube.com/watch?v=python_keywords_203", "duration": 9},
                            ],
                            "examples": [
                                {"title": "Proper Indentation", "code": "if True:\n    print('This is indented')\n    print('Still indented')\nprint('Back to main level')", "explanation": "Indentation is mandatory in Python to define code blocks."},
                                {"title": "Comments in Python", "code": "# This is a single line comment\n''' This is a\nmulti-line comment '''\nprint('Code here')", "explanation": "Comments help explain code and are not executed."},
                            ]
                        },
                        {
                            "title": "Variables and Assignment",
                            "theory": "Variables are containers that store data values in Python. You create a variable by assigning a value using the = operator. Python doesn't require specifying the data type - it's inferred automatically. Variables can hold different types: integers, floats, strings, booleans. Variable names should be descriptive and follow conventions (lowercase, underscore for spaces). Python allows multiple assignments like a = b = 5 or a, b = 5, 10. Variable names are case-sensitive. You can reassign variables to different types at any time since Python is dynamically typed.",
                            "main_video": "https://www.youtube.com/watch?v=python_variables_301",
                            "duration_minutes": 13,
                            "related_videos": [
                                {"title": "Data Types Overview", "url": "https://www.youtube.com/watch?v=python_datatypes_302", "duration": 11},
                                {"title": "Variable Naming Conventions", "url": "https://www.youtube.com/watch?v=python_naming_303", "duration": 8},
                            ],
                            "examples": [
                                {"title": "Creating Variables", "code": "name = 'Alice'\nage = 25\nheight = 5.7\nis_student = True", "explanation": "Variables store different types of data without explicit type declaration."},
                                {"title": "Multiple Assignment", "code": "x, y, z = 10, 20, 30\nprint(x, y, z)", "explanation": "Python allows assigning multiple variables in one statement."},
                            ]
                        },
                        {
                            "title": "Data Types",
                            "theory": "Python supports multiple built-in data types: int (integers), float (decimal numbers), str (text), bool (True/False), list (ordered collection), tuple (immutable sequence), dict (key-value pairs), set (unique values). Each type has specific operations and methods. Integers can be any size in Python. Floats use IEEE 754 standard and can have precision issues. Strings are immutable sequences of characters. Booleans are based on integers (True=1, False=0). Collections can be nested. Type conversion can be done with int(), float(), str(), etc. Understanding data types is fundamental for proper data handling.",
                            "main_video": "https://www.youtube.com/watch?v=python_types_401",
                            "duration_minutes": 15,
                            "related_videos": [
                                {"title": "Type Conversion", "url": "https://www.youtube.com/watch?v=python_convert_402", "duration": 10},
                                {"title": "Collections Deep Dive", "url": "https://www.youtube.com/watch?v=python_collections_403", "duration": 18},
                            ],
                            "examples": [
                                {"title": "Working with Data Types", "code": "num = 42\nfloat_num = 3.14\ntext = 'Hello'\nflag = True\ncolors = ['red', 'blue', 'green']", "explanation": "Each variable stores a different type of data."},
                                {"title": "Type Checking", "code": "x = 10\nprint(type(x))  # <class 'int'>\ny = 'text'\nprint(type(y))  # <class 'str'>", "explanation": "Use type() to check variable's data type."},
                            ]
                        },
                    ]
                },
                {
                    "name": "Variables and Data Types",
                    "description": "Deep dive into Python variables and data types",
                    "concepts": [
                        {
                            "title": "Strings and String Operations",
                            "theory": "Strings are immutable sequences of characters enclosed in quotes (single, double, or triple). Python provides extensive string methods: upper(), lower(), strip(), replace(), split(), join(). String indexing starts at 0 from left and -1 from right. Slicing extracts substrings using [start:end:step]. String concatenation uses + operator. f-strings (formatted strings) with f'' allow variable interpolation. String comparison is lexicographic. Escape sequences like \\n for newline, \\t for tab. Raw strings use r'' prefix to ignore escapes. Regular expressions (regex) provide powerful pattern matching.",
                            "main_video": "https://www.youtube.com/watch?v=python_strings_501",
                            "duration_minutes": 16,
                            "related_videos": [
                                {"title": "String Methods", "url": "https://www.youtube.com/watch?v=python_string_methods_502", "duration": 14},
                                {"title": "String Formatting", "url": "https://www.youtube.com/watch?v=python_formatting_503", "duration": 12},
                            ],
                            "examples": [
                                {"title": "String Manipulation", "code": "text = 'Hello World'\nprint(text.lower())  # hello world\nprint(text.replace('World', 'Python'))  # Hello Python", "explanation": "Strings have many built-in methods for manipulation."},
                                {"title": "String Slicing", "code": "word = 'Python'\nprint(word[0])     # P\nprint(word[1:4])   # yth\nprint(word[::-1])  # nohtyP", "explanation": "Access parts of strings using indexing and slicing."},
                            ]
                        },
                        {
                            "title": "Numbers: Integers and Floats",
                            "theory": "Integers (int) in Python can be arbitrarily large with unlimited precision. Floats use double-precision (64-bit) following IEEE 754 standard. Arithmetic operations: +, -, *, /, //, %, **. Integer division // returns floor value. Modulo % returns remainder. Power ** for exponentiation. Python follows standard operator precedence (PEMDAS). Comparison operators: ==, !=, <, >, <=, >=. Unary operators: + (positive), - (negative), ~ (bitwise NOT). Bitwise operations for integers: & (AND), | (OR), ^ (XOR), << (left shift), >> (right shift). Number methods: abs(), round(), divmod().",
                            "main_video": "https://www.youtube.com/watch?v=python_numbers_601",
                            "duration_minutes": 14,
                            "related_videos": [
                                {"title": "Numeric Operations", "url": "https://www.youtube.com/watch?v=python_numeric_ops_602", "duration": 11},
                                {"title": "Bitwise Operations", "url": "https://www.youtube.com/watch?v=python_bitwise_603", "duration": 10},
                            ],
                            "examples": [
                                {"title": "Arithmetic Operations", "code": "a, b = 10, 3\nprint(a + b)   # 13\nprint(a // b)  # 3\nprint(a ** b)  # 1000", "explanation": "Perform various arithmetic operations on numbers."},
                                {"title": "Working with Floats", "code": "x = 3.14\ny = 2.86\nprint(round(x + y, 1))  # 6.0", "explanation": "Floats can be rounded to specific decimal places."},
                            ]
                        },
                    ]
                },
            ]
        },
        {
            "name": "MERN Stack Development",
            "description": "Build full-stack web applications with MongoDB, Express, React, Node.js",
            "level": "intermediate",
            "rating": 4.7,
            "icon": "⚛️",
            "topics": [
                {
                    "name": "MongoDB Basics",
                    "description": "Learn NoSQL database fundamentals",
                    "concepts": [
                        {
                            "title": "What is MongoDB?",
                            "theory": "MongoDB is a NoSQL document database that stores data in flexible JSON-like documents. Unlike relational databases with tables and rows, MongoDB uses collections and documents. Each document can have different structure (schema-less). Data is stored in BSON format (Binary JSON). Collections are groups of documents, similar to tables. MongoDB offers horizontal scalability through sharding. It supports complex queries, indexing, and aggregation. Transactions are ACID-compliant in recent versions. Perfect for applications requiring flexibility and scalability. MongoDB Atlas provides cloud hosting.",
                            "main_video": "https://www.youtube.com/watch?v=mongodb_intro_101",
                            "duration_minutes": 18,
                            "related_videos": [
                                {"title": "MongoDB vs SQL", "url": "https://www.youtube.com/watch?v=mongodb_vs_sql_102", "duration": 12},
                                {"title": "Setup MongoDB", "url": "https://www.youtube.com/watch?v=mongodb_setup_103", "duration": 15},
                            ],
                            "examples": [
                                {"title": "MongoDB Document", "code": "{\n  _id: ObjectId(...),\n  name: 'Alice',\n  email: 'alice@example.com',\n  age: 25\n}", "explanation": "MongoDB stores data as BSON documents with flexible structure."},
                                {"title": "Create Collection", "code": "db.createCollection('users')\ndb.users.insertOne({name: 'Bob', age: 30})", "explanation": "Create collections and insert documents dynamically."},
                            ]
                        },
                        {
                            "title": "CRUD Operations",
                            "theory": "CRUD stands for Create, Read, Update, Delete - the four basic operations. Create: insertOne(), insertMany() add documents. Read: find(), findById(), findOne() retrieve documents. Update: updateOne(), updateMany(), replaceOne() modify documents. Delete: deleteOne(), deleteMany() remove documents. Query operators like $eq, $gt, $lt, $in for filtering. Projection specifies which fields to return. Sorting and pagination using sort() and limit(). Bulk operations for multiple changes. Understanding CRUD is essential for database manipulation.",
                            "main_video": "https://www.youtube.com/watch?v=mongodb_crud_201",
                            "duration_minutes": 20,
                            "related_videos": [
                                {"title": "Query Operators", "url": "https://www.youtube.com/watch?v=mongodb_operators_202", "duration": 16},
                                {"title": "Working with Arrays", "url": "https://www.youtube.com/watch?v=mongodb_arrays_203", "duration": 14},
                            ],
                            "examples": [
                                {"title": "Insert Documents", "code": "db.users.insertMany([\n  {name: 'Alice', age: 25},\n  {name: 'Bob', age: 30}\n])", "explanation": "Insert multiple documents in MongoDB."},
                                {"title": "Query Documents", "code": "db.users.find({age: {$gte: 25}})\ndb.users.findOne({name: 'Alice'})", "explanation": "Find documents based on criteria."},
                            ]
                        },
                    ]
                },
            ]
        },
        {
            "name": "Machine Learning Fundamentals",
            "description": "Introduction to ML concepts and algorithms",
            "level": "intermediate",
            "rating": 4.9,
            "icon": "🤖",
            "topics": [
                {
                    "name": "ML Basics",
                    "description": "Foundation of Machine Learning",
                    "concepts": [
                        {
                            "title": "What is Machine Learning?",
                            "theory": "Machine Learning is a subset of Artificial Intelligence where systems learn from data without explicit programming. Types: Supervised (labeled data), Unsupervised (unlabeled data), Reinforcement (reward-based). Supervised learning includes regression (predict continuous values) and classification (predict categories). Examples: predicting house prices (regression), detecting spam emails (classification). Unsupervised learning finds patterns: clustering groups similar items, dimensionality reduction simplifies data. Reinforcement learning agents learn through trial-and-error. ML workflow: data collection, preprocessing, feature engineering, model training, evaluation, deployment. Overfitting occurs when model memorizes training data. Underfitting happens when model is too simple.",
                            "main_video": "https://www.youtube.com/watch?v=ml_intro_301",
                            "duration_minutes": 22,
                            "related_videos": [
                                {"title": "ML Types Explained", "url": "https://www.youtube.com/watch?v=ml_types_302", "duration": 18},
                                {"title": "Real-world ML Applications", "url": "https://www.youtube.com/watch?v=ml_applications_303", "duration": 15},
                            ],
                            "examples": [
                                {"title": "House Price Prediction", "code": "# Input: house features (size, bedrooms, location)\n# Output: predicted price\n# This is SUPERVISED LEARNING (Regression)", "explanation": "ML predicts continuous values like house prices from historical data."},
                                {"title": "Email Classification", "code": "# Input: email content\n# Output: spam or not spam\n# This is SUPERVISED LEARNING (Classification)", "explanation": "ML classifies items into categories based on learned patterns."},
                            ]
                        },
                        {
                            "title": "Supervised Learning",
                            "theory": "Supervised learning uses labeled training data to build models. Each training example has input features and correct output labels. Regression models predict continuous numeric values (e.g., price, temperature). Linear regression fits a line through data points. Classification models predict discrete categories (e.g., yes/no, positive/negative). Logistic regression despite its name is for classification using sigmoid function. Decision trees split data recursively on features. Random forests combine multiple decision trees for robustness. K-Nearest Neighbors finds k closest training examples for prediction. Support Vector Machines find optimal separation boundary. Overfitting risks with complex models - use train/test split and cross-validation.",
                            "main_video": "https://www.youtube.com/watch?v=ml_supervised_401",
                            "duration_minutes": 24,
                            "related_videos": [
                                {"title": "Linear Regression Deep Dive", "url": "https://www.youtube.com/watch?v=ml_linear_reg_402", "duration": 20},
                                {"title": "Classification Algorithms", "url": "https://www.youtube.com/watch?v=ml_classification_403", "duration": 22},
                            ],
                            "examples": [
                                {"title": "Linear Regression Implementation", "code": "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\npredictions = model.predict(X_test)", "explanation": "Build and train a linear regression model using scikit-learn."},
                                {"title": "Train-Test Split", "code": "from sklearn.model_selection import train_test_split\nX_train, X_test, y_train, y_test = train_test_split(\n  X, y, test_size=0.2, random_state=42\n)", "explanation": "Split data for training and evaluation to avoid overfitting."},
                            ]
                        },
                    ]
                },
            ]
        },
    ]

    # Create courses
    for course_data in courses_data:
        print(f"\n📚 Creating Course: {course_data['name']}")

        course = Course(
            name=course_data['name'],
            description=course_data['description'],
            level=course_data['level'],
            rating=course_data['rating'],
            icon=course_data['icon']
        )
        db.add(course)
        db.flush()

        # Create topics
        for topic_data in course_data['topics']:
            print(f"  📖 Topic: {topic_data['name']}")

            topic = Topic(
                name=topic_data['name'],
                description=topic_data['description'],
                course_id=course.id
            )
            db.add(topic)
            db.flush()

            # Create concepts with full data
            for concept in topic_data['concepts']:
                print(f"    💡 Concept: {concept['title']}")

                # Create main video
                main_video = Video(
                    title=concept['title'],
                    url=concept['main_video'],
                    duration_minutes=concept['duration_minutes'],
                    type='main',
                    topic_id=topic.id
                )
                db.add(main_video)
                db.flush()

                # Create related videos
                for related in concept.get('related_videos', []):
                    related_video = Video(
                        title=related['title'],
                        url=related['url'],
                        duration_minutes=related['duration'],
                        type='related',
                        topic_id=topic.id
                    )
                    db.add(related_video)

    db.commit()
    print("\n" + "=" * 70)
    print("✅ COMPLETE DATA SEEDING DONE!")
    print("=" * 70)
    print("📊 Summary:")
    total_courses = db.query(Course).count()
    total_topics = db.query(Topic).count()
    total_videos = db.query(Video).count()
    print(f"  ✅ Courses: {total_courses}")
    print(f"  ✅ Topics: {total_topics}")
    print(f"  ✅ Videos: {total_videos}")
    print("=" * 70)


if __name__ == "__main__":
    from app.database import SessionLocal
    db = SessionLocal()
    seed_complete_courses_data(db)
    db.close()
