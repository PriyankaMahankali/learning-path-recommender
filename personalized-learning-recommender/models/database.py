import sqlite3
from datetime import datetime


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_FILE = "data/learning_assistant.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    """Create and return a database connection."""

    return sqlite3.connect(
        DATABASE_FILE,
        check_same_thread=False
    )


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():
    """Create required database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            goal TEXT,
            experience TEXT,
            learning_preference TEXT,
            interests TEXT DEFAULT '',
            created_at TEXT
        )
        """
    )

    # -----------------------------------------------------
    # Add interests column to old database if necessary
    # -----------------------------------------------------

    try:

        cursor.execute(
            "ALTER TABLE users ADD COLUMN interests TEXT DEFAULT ''"
        )

    except sqlite3.OperationalError:

        # Column already exists
        pass

    # -----------------------------------------------------
    # USER SKILLS
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            status TEXT DEFAULT 'completed',
            completed_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """
    )

    # -----------------------------------------------------
    # COMPLETED COURSES
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS completed_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """
    )

    # -----------------------------------------------------
    # FEEDBACK
    # -----------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course TEXT NOT NULL,
            feedback TEXT,
            difficulty TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """
    )

    connection.commit()
    connection.close()


# =========================================================
# CREATE USER
# =========================================================

def create_user(
    username,
    password,
    name,
    goal="",
    experience="",
    learning_preference="",
    interests=""
):
    """Create a new learner account."""

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                name,
                goal,
                experience,
                learning_preference,
                interests,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (
                username.strip(),
                password,
                name.strip(),
                goal.strip(),
                experience,
                learning_preference,
                interests.strip(),
                datetime.now().isoformat()
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

        connection.close()

        return user_id

    except sqlite3.IntegrityError:

        connection.close()

        return None


# =========================================================
# LOGIN
# =========================================================

def login_user(username, password):
    """Authenticate learner."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            username,
            name,
            goal,
            experience,
            learning_preference,
            interests

        FROM users

        WHERE username = ?
        AND password = ?
        """,

        (
            username.strip(),
            password
        )
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return None

    return {

        "user_id": row[0],

        "username": row[1],

        "name": row[2],

        "goal": row[3] or "",

        "experience": row[4] or "Beginner",

        "learning_preference":
            row[5] or "Mixed",

        "interests":
            row[6] or ""

    }


# =========================================================
# GET USER
# =========================================================

def get_user(user_id):
    """Retrieve learner profile."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            username,
            name,
            goal,
            experience,
            learning_preference,
            interests

        FROM users

        WHERE user_id = ?
        """,

        (user_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return None

    return {

        "user_id": row[0],
        "username": row[1],
        "name": row[2],
        "goal": row[3] or "",
        "experience": row[4] or "Beginner",
        "learning_preference": row[5] or "Mixed",
        "interests": row[6] or ""

    }


# =========================================================
# UPDATE PROFILE
# =========================================================

def update_user_profile(
    user_id,
    name,
    goal,
    experience,
    learning_preference,
    interests=""
):
    """Update learner profile."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users

        SET
            name = ?,
            goal = ?,
            experience = ?,
            learning_preference = ?,
            interests = ?

        WHERE user_id = ?
        """,

        (
            name.strip(),
            goal.strip(),
            experience,
            learning_preference,
            interests.strip(),
            user_id
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# SAVE USER SKILL
# =========================================================

def save_user_skill(user_id, skill):
    """Save a completed/known skill."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id

        FROM user_skills

        WHERE user_id = ?

        AND LOWER(skill) = LOWER(?)
        """,

        (
            user_id,
            skill.strip()
        )
    )

    existing = cursor.fetchone()

    if existing is None:

        cursor.execute(
            """
            INSERT INTO user_skills
            (
                user_id,
                skill,
                status,
                completed_at
            )

            VALUES (?, ?, ?, ?)
            """,

            (
                user_id,
                skill.strip(),
                "completed",
                datetime.now().isoformat()
            )
        )

    connection.commit()
    connection.close()


# =========================================================
# GET COMPLETED SKILLS
# =========================================================

def get_completed_skills(user_id):
    """Get all previously completed skills."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT skill

        FROM user_skills

        WHERE user_id = ?

        AND status = 'completed'
        """,

        (user_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        row[0]
        for row in rows
    ]


# =========================================================
# SAVE COMPLETED COURSE
# =========================================================

def save_completed_course(
    user_id,
    course
):
    """Save completed course."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id

        FROM completed_courses

        WHERE user_id = ?

        AND LOWER(course) = LOWER(?)
        """,

        (
            user_id,
            course.strip()
        )
    )

    existing = cursor.fetchone()

    if existing is None:

        cursor.execute(
            """
            INSERT INTO completed_courses
            (
                user_id,
                course,
                completed_at
            )

            VALUES (?, ?, ?)
            """,

            (
                user_id,
                course.strip(),
                datetime.now().isoformat()
            )
        )

    connection.commit()
    connection.close()


# =========================================================
# GET COMPLETED COURSES
# =========================================================

def get_completed_courses(user_id):
    """Get all completed courses."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT course

        FROM completed_courses

        WHERE user_id = ?
        """,

        (user_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        row[0]
        for row in rows
    ]


# =========================================================
# SAVE FEEDBACK
# =========================================================

def save_user_feedback(
    user_id,
    course,
    feedback,
    difficulty
):
    """Save recommendation feedback."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO feedback
        (
            user_id,
            course,
            feedback,
            difficulty,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            user_id,
            course,
            feedback,
            difficulty,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# GET USER FEEDBACK
# =========================================================

def get_user_feedback(user_id):
    """Get learner feedback."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            course,
            feedback,
            difficulty

        FROM feedback

        WHERE user_id = ?

        ORDER BY created_at ASC
        """,

        (user_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "course": row[0],
            "feedback": row[1],
            "difficulty": row[2]
        }

        for row in rows
    ]