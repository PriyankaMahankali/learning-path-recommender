def save_feedback(
    feedback_list,
    course_title,
    feedback,
    difficulty
):
    """
    Save or update feedback for a course.

    Each course has only one feedback record.
    If the learner changes their feedback,
    the previous record is updated.
    """

    new_record = {
        "course": course_title,
        "feedback": feedback,
        "difficulty": difficulty
    }

    # Check whether feedback already exists
    for item in feedback_list:

        if item["course"] == course_title:

            item["feedback"] = feedback
            item["difficulty"] = difficulty

            return feedback_list

    # If no previous feedback exists
    feedback_list.append(new_record)

    return feedback_list


def get_feedback_summary(feedback_list):
    """
    Count useful and not useful feedback.
    """

    positive = 0
    negative = 0

    for item in feedback_list:

        if item["feedback"] == "Useful":
            positive += 1

        elif item["feedback"] == "Not Useful":
            negative += 1

    return positive, negative


def get_difficulty_summary(feedback_list):
    """
    Count learner difficulty feedback.
    """

    easy = 0
    moderate = 0
    difficult = 0

    for item in feedback_list:

        if item["difficulty"] == "Easy":
            easy += 1

        elif item["difficulty"] == "Moderate":
            moderate += 1

        elif item["difficulty"] == "Difficult":
            difficult += 1

    return easy, moderate, difficult