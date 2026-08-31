def calculate_progress(learning_path, completed_skills):
    """
    Calculate learner progress based on completed skills.
    """

    if not learning_path:
        return 0

    completed_count = sum(
        1
        for skill in learning_path
        if skill in completed_skills
    )

    progress = completed_count / len(learning_path)

    return progress


def get_next_skill(learning_path, completed_skills):
    """
    Find the next incomplete skill in the learning path.
    """

    for skill in learning_path:

        if skill not in completed_skills:
            return skill

    return None