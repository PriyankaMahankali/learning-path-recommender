import pandas as pd


def load_skill_data():
    """Load the career skill database."""

    return pd.read_csv(
        "data/skills.csv",
        keep_default_na=False
    )


def find_goal(goal, skill_data):
    """Find the closest supported career goal."""

    goal = str(goal).strip().lower()

    for available_goal in skill_data["goal"].unique():

        available_goal = str(
            available_goal
        ).strip().lower()

        if (
            available_goal in goal
            or goal in available_goal
        ):
            return available_goal.title()

    return None


def analyze_skill_gap(
    goal,
    current_skills,
    completed_skills=None
):
    """
    Analyze the learner's skill gap.

    current_skills:
        Skills entered in the current profile.

    completed_skills:
        Skills previously completed and stored
        in the learner database.
    """

    skill_data = load_skill_data()


    # -----------------------------------------------------
    # Combine current + previously completed skills
    # -----------------------------------------------------

    if completed_skills is None:
        completed_skills = []


    all_known_skills = (

        list(current_skills)

        + list(completed_skills)

    )


    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    known_skill_set = {

        str(skill).strip().lower()

        for skill in all_known_skills

        if str(skill).strip()

    }


    # -----------------------------------------------------
    # Find career
    # -----------------------------------------------------

    matched_goal = find_goal(
        goal,
        skill_data
    )


    if matched_goal is None:

        return None, [], []


    # -----------------------------------------------------
    # Get required skills
    # -----------------------------------------------------

    required = skill_data[

        skill_data["goal"]
        .astype(str)
        .str.strip()
        .str.lower()

        == matched_goal.strip().lower()

    ]


    required_skills = (

        required["skill"]

        .astype(str)

        .str.strip()

        .tolist()

    )


    # -----------------------------------------------------
    # Separate known and missing skills
    # -----------------------------------------------------

    known_skills = []

    missing_skills = []


    for skill in required_skills:

        if skill.lower() in known_skill_set:

            known_skills.append(skill)

        else:

            missing_skills.append(skill)


    return (

        matched_goal,

        known_skills,

        missing_skills

    )