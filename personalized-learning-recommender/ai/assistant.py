def get_assistant_response(
    question,
    profile,
    known_skills,
    missing_skills,
    learning_path,
    completed_skills
):
    """
    Generate a personalized response using
    the learner's profile, skill gaps,
    learning path and progress.
    """

    question = question.lower().strip()

    goal = profile.get("goal", "")
    experience = profile.get("experience", "")
    interests = profile.get("interests", [])

    # =====================================================
    # CURRENT PROGRESS
    # =====================================================

    total_skills = len(learning_path)

    completed_count = len(completed_skills)

    if total_skills > 0:
        progress = (
            completed_count / total_skills
        ) * 100
    else:
        progress = 0

    next_skill = None

    for skill in learning_path:

        if skill not in completed_skills:

            next_skill = skill
            break

    # =====================================================
    # QUESTION: WHAT SHOULD I LEARN NEXT?
    # =====================================================

    if (
        "what should i learn next" in question
        or "what do i learn next" in question
        or "next skill" in question
        or "learn next" in question
    ):

        if next_skill:

            return (
                f"### 🎯 Your Next Learning Step\n\n"
                f"Based on your current progress, "
                f"you should learn **{next_skill}** next.\n\n"
                f"You have completed "
                f"**{completed_count} out of {total_skills}** "
                f"skills ({progress:.0f}% progress).\n\n"
                f"💡 I recommend completing **{next_skill}** "
                f"before moving further along your learning path."
            )

        return (
            "### 🏆 Learning Path Completed!\n\n"
            "You have completed all the skills "
            "in your current learning path."
        )

    # =====================================================
    # QUESTION: WHAT ARE MY MISSING SKILLS?
    # =====================================================

    if (
        "what skills am i missing" in question
        or "missing skills" in question
        or "skills do i need" in question
        or "skills i need" in question
    ):

        if missing_skills:

            skill_text = ", ".join(
                missing_skills
            )

            return (
                "### ⚠️ Your Skill Gaps\n\n"
                f"For your goal of **{goal}**, "
                f"the skills you still need to develop are:\n\n"
                f"**{skill_text}**\n\n"
                "These skills form the basis of your "
                "personalized learning path."
            )

        return (
            "### 🎉 No Major Skill Gaps\n\n"
            "You currently have all the skills "
            "required by the selected skill map."
        )

    # =====================================================
    # QUESTION: WHAT SKILLS DO I KNOW?
    # =====================================================

    if (
        "what skills do i already know" in question
        or "skills do i know" in question
        or "my current skills" in question
        or "skills i already know" in question
    ):

        if known_skills:

            skill_text = ", ".join(
                known_skills
            )

            return (
                "### ✅ Your Current Skills\n\n"
                f"You currently know:\n\n"
                f"**{skill_text}**\n\n"
                f"These skills are considered when "
                f"generating your personalized recommendations."
            )

        return (
            "### 📝 Current Skills\n\n"
            "No matching skills were identified "
            "in your learner profile."
        )

    # =====================================================
    # QUESTION: PROGRESS
    # =====================================================

    if (
        "what is my progress" in question
        or "my progress" in question
        or "how much progress" in question
        or "progress" in question
    ):

        return (
            "### 📊 Your Learning Progress\n\n"
            f"**Completed:** {completed_count}/{total_skills} skills\n\n"
            f"**Progress:** {progress:.0f}%\n\n"
            f"**Current Focus:** "
            f"{next_skill if next_skill else 'Learning path completed'}"
        )

    # =====================================================
    # QUESTION: WHY DO I NEED A SKILL?
    # =====================================================

    if (
        "why do i need" in question
        or "why do i need machine learning" in question
        or "why is machine learning needed" in question
    ):

        return (
            "### 🧠 Why Machine Learning?\n\n"
            "Machine Learning is an important part of "
            f"your **{goal}** learning path.\n\n"
            "It provides the foundation for building "
            "models that can learn patterns from data "
            "and make predictions.\n\n"
            "It also comes before several later skills "
            "in your current roadmap, including "
            "Deep Learning and Model Deployment."
        )

    # =====================================================
    # QUESTION: CAN I SKIP DEEP LEARNING?
    # =====================================================

    if (
        "skip deep learning" in question
        or "without deep learning" in question
        or "do i need deep learning" in question
    ):

        return (
            "### 🧠 About Deep Learning\n\n"
            "You do not necessarily need to complete "
            "Deep Learning before every skill in your roadmap.\n\n"
            "In your current learning path, "
            "**Deep Learning is a prerequisite for "
            "Neural Networks**, but it is not the "
            "prerequisite for Model Deployment.\n\n"
            "So the roadmap contains different learning branches."
        )

    # =====================================================
    # QUESTION: MODEL DEPLOYMENT BEFORE DEEP LEARNING
    # =====================================================

    if (
        "model deployment" in question
        and (
            "before deep learning" in question
            or "without deep learning" in question
            or "skip deep learning" in question
            or "do model deployment" in question
        )
    ):

        return (
            "### 🚀 Model Deployment vs Deep Learning\n\n"
            "**Yes — based on your current roadmap, "
            "you can complete Model Deployment without "
            "completing Deep Learning first.**\n\n"
            "Your prerequisite structure is:\n\n"
            "• Statistics → Machine Learning\n"
            "• Machine Learning → Deep Learning\n"
            "• Deep Learning → Neural Networks\n"
            "• Machine Learning → Model Deployment\n"
            "• Model Deployment → MLOps\n\n"
            "Therefore, once you complete "
            "**Machine Learning**, Model Deployment "
            "can become available even if Deep Learning "
            "is still incomplete.\n\n"
            "💡 Your roadmap treats Deep Learning and "
            "Model Deployment as separate branches after "
            "Machine Learning."
        )

    # =====================================================
    # QUESTION: WHY WAS A SKILL RECOMMENDED?
    # =====================================================

    if (
        "why was a skill recommended" in question
        or "why was this skill recommended" in question
        or "why recommended" in question
    ):

        return (
            "### 💡 Why Skills Are Recommended\n\n"
            "Your learning path is generated using "
            "your target goal, current skills and "
            "identified skill gaps.\n\n"
            "Skills that are missing from your profile "
            "are prioritized according to their "
            "prerequisites."
        )

    # =====================================================
    # QUESTION: GOAL
    # =====================================================

    if (
        "what is my goal" in question
        or "my goal" in question
    ):

        return (
            "### 🎯 Your Learning Goal\n\n"
            f"Your current goal is:\n\n"
            f"**{goal}**\n\n"
            f"Your experience level is **{experience}**."
        )

    # =====================================================
    # DEFAULT RESPONSE
    # =====================================================

    return (
        "### 🤖 Your AI Learning Assistant\n\n"
        f"I can help you with your **{goal}** "
        "learning journey.\n\n"
        "Try asking:\n\n"
        "• What should I learn next?\n"
        "• What skills am I missing?\n"
        "• What skills do I already know?\n"
        "• What is my progress?\n"
        "• Why do I need Machine Learning?\n"
        "• Can I skip Deep Learning?\n"
        "• Can I do Model Deployment before Deep Learning?\n"
        "• Why was a skill recommended?"
    )