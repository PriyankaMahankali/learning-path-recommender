import pandas as pd


def load_courses():
    """Load the course database."""
    return pd.read_csv("data/courses.csv")


def recommend_courses(
    missing_skills,
    experience_level,
    learning_preference
):
    """
    Recommend courses based on missing skills,
    learner experience and learning preference.
    """

    courses = load_courses()

    recommendations = []

    for _, course in courses.iterrows():

        # Check whether course teaches a missing skill
        if course["skill"] not in missing_skills:
            continue

        score = 0

        # -------------------------
        # Skill Match
        # -------------------------

        score += 5

        # -------------------------
        # Experience Match
        # -------------------------

        if course["level"] == experience_level:
            score += 3

        elif (
            experience_level == "Beginner"
            and course["level"] == "Intermediate"
        ):
            score += 1

        elif (
            experience_level == "Intermediate"
            and course["level"] == "Advanced"
        ):
            score += 1

        # -------------------------
        # Learning Preference
        # -------------------------

        if learning_preference == "Video Courses":
            if course["type"] == "Course":
                score += 2

        elif learning_preference == "Mixed":
            score += 1

        # -------------------------
        # Store Recommendation
        # -------------------------

        recommendations.append({
            "title": course["title"],
            "skill": course["skill"],
            "level": course["level"],
            "duration": course["duration"],
            "description": course["description"],
            "score": score
        })

    # Sort by recommendation score
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations