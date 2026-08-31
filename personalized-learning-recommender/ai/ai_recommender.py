import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# LOAD COURSE DATABASE
# =========================================================

def load_courses():
    """Load the course database."""

    return pd.read_csv(
        "data/courses.csv",
        keep_default_na=False
    )


# =========================================================
# LOAD SKILL DATABASE
# =========================================================

def load_skill_data():
    """Load career skill and prerequisite data."""

    return pd.read_csv(
        "data/skills.csv",
        keep_default_na=False
    )


# =========================================================
# FIND REQUIRED SKILLS FOR CAREER
# =========================================================

def get_goal_skills(goal):
    """
    Get all skills associated with the selected
    career goal.
    """

    skill_data = load_skill_data()

    goal_text = str(
        goal
    ).strip().lower()


    # Find matching career goal
    matching_goals = []

    for available_goal in skill_data["goal"].unique():

        available_goal = str(
            available_goal
        ).strip()

        if (
            available_goal.lower() in goal_text
            or goal_text in available_goal.lower()
        ):

            matching_goals.append(
                available_goal
            )


    if not matching_goals:

        return []


    selected_goal = matching_goals[0]


    # Get skills for selected career
    required_rows = skill_data[
        skill_data["goal"]
        .astype(str)
        .str.strip()
        .str.lower()
        == selected_goal.lower()
    ]


    required_skills = (
        required_rows["skill"]
        .astype(str)
        .str.strip()
        .tolist()
    )


    return required_skills


# =========================================================
# AI RECOMMENDATION ENGINE
# =========================================================

def get_ai_recommendations(
    goal,
    interests,
    missing_skills,
    experience_level,
    learning_preference,
    feedback_list=None
):
    """
    Generate personalized course recommendations.

    Uses:

    1. Career-specific course filtering
    2. TF-IDF
    3. Cosine similarity
    4. Skill-gap matching
    5. Experience matching
    6. Learner feedback
    """


    # =====================================================
    # LOAD DATA
    # =====================================================

    courses = load_courses()


    if feedback_list is None:

        feedback_list = []


    if courses.empty:

        return []


    # =====================================================
    # GET CAREER-SPECIFIC SKILLS
    # =====================================================

    goal_skills = get_goal_skills(
        goal
    )


    if not goal_skills:

        return []


    # Normalize goal skills
    goal_skill_set = {

        str(skill)
        .strip()
        .lower()

        for skill in goal_skills

    }


    # =====================================================
    # FILTER COURSES BY CAREER
    # =====================================================

    courses = courses[
        courses["skill"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(goal_skill_set)
    ].copy()


    if courses.empty:

        return []


    # =====================================================
    # NORMALIZE MISSING SKILLS
    # =====================================================

    missing_skill_set = {

        str(skill)
        .strip()
        .lower()

        for skill in missing_skills

    }


    # =====================================================
    # LEARNER PROFILE TEXT
    # =====================================================

    learner_text = (

        str(goal) + " "

        + str(interests) + " "

        + " ".join(
            str(skill)
            for skill in missing_skills
        ) + " "

        + str(experience_level) + " "

        + str(learning_preference)

    )


    # =====================================================
    # COURSE TEXT
    # =====================================================

    course_text = (

        courses["title"]
        .fillna("")
        .astype(str)

        + " "

        + courses["skill"]
        .fillna("")
        .astype(str)

        + " "

        + courses["level"]
        .fillna("")
        .astype(str)

        + " "

        + courses["description"]
        .fillna("")
        .astype(str)

    )


    # =====================================================
    # TF-IDF VECTORIZATION
    # =====================================================

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )


    all_text = (
        [learner_text]
        + course_text.tolist()
    )


    tfidf_matrix = vectorizer.fit_transform(
        all_text
    )


    # =====================================================
    # COSINE SIMILARITY
    # =====================================================

    similarity_scores = cosine_similarity(

        tfidf_matrix[0:1],

        tfidf_matrix[1:]

    ).flatten()


    courses["similarity"] = (
        similarity_scores
    )


    # =====================================================
    # SKILL GAP MATCH
    # =====================================================

    courses["skill_match"] = (

        courses["skill"]
        .astype(str)
        .str.strip()
        .str.lower()
        .apply(

            lambda skill:

            1
            if skill in missing_skill_set
            else 0

        )

    )


    # =====================================================
    # EXPERIENCE MATCH
    # =====================================================

    courses["experience_match"] = (

        courses["level"]
        .astype(str)
        .str.strip()
        .str.lower()
        .apply(

            lambda level:

            1
            if level
            == str(experience_level)
            .strip()
            .lower()

            else 0

        )

    )


    # =====================================================
    # FEEDBACK SCORE
    # =====================================================

    courses["feedback_score"] = 0.0


    for feedback in feedback_list:

        course_title = feedback.get(
            "course"
        )

        feedback_type = feedback.get(
            "feedback"
        )

        difficulty = feedback.get(
            "difficulty"
        )


        # ---------------------------------------------
        # USEFULNESS FEEDBACK
        # ---------------------------------------------

        if feedback_type == "Useful":

            courses.loc[
                courses["title"] == course_title,
                "feedback_score"
            ] += 2


        elif feedback_type == "Not Useful":

            courses.loc[
                courses["title"] == course_title,
                "feedback_score"
            ] -= 2


        # ---------------------------------------------
        # DIFFICULTY FEEDBACK
        # ---------------------------------------------

        if difficulty == "Easy":

            courses.loc[
                courses["title"] == course_title,
                "feedback_score"
            ] += 0.5


        elif difficulty == "Difficult":

            courses.loc[
                courses["title"] == course_title,
                "feedback_score"
            ] -= 1


    # =====================================================
    # EXPLAINABLE RECOMMENDATION COMPONENTS
    # =====================================================

    courses["similarity_score"] = (

        courses["similarity"] * 5

    )


    courses["skill_gap_score"] = (

        courses["skill_match"] * 3

    )


    courses["experience_score"] = (

        courses["experience_match"] * 2

    )


    # =====================================================
    # FINAL PERSONALIZATION SCORE
    # =====================================================

    courses["final_score"] = (

        courses["similarity_score"]

        + courses["skill_gap_score"]

        + courses["experience_score"]

        + courses["feedback_score"]

    )


    # =====================================================
    # SORT RECOMMENDATIONS
    # =====================================================

    courses = courses.sort_values(

        by="final_score",

        ascending=False

    )


    # =====================================================
    # RETURN TOP 6
    # =====================================================

    return courses.head(
        6
    ).to_dict(
        "records"
    )