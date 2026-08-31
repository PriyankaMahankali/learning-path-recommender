import pandas as pd
import streamlit as st

from ai.ai_recommender import get_ai_recommendations
from ai.assistant import get_assistant_response

from models.feedback import (
    get_difficulty_summary,
    get_feedback_summary,
    save_feedback
)

from models.path_generator import generate_learning_path
from models.projects import get_project_recommendation
from models.progress import calculate_progress, get_next_skill
from models.skill_gap import analyze_skill_gap

from models.database import (
    initialize_database,
    create_user,
    login_user,
    update_user_profile,
    save_user_skill,
    get_completed_skills,
    save_completed_course,
    get_completed_courses,
    save_user_feedback,
    get_user_feedback
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Personalized Learning Assistant",
    page_icon="🎓",
    layout="wide"
)

initialize_database()


# =========================================================
# CUSTOM UI
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    h1 {
        font-size: 40px !important;
        font-weight: 700 !important;
    }

    h2 {
        font-weight: 650 !important;
    }

    h3 {
        font-weight: 600 !important;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    [data-testid="stMetric"] {
        border-radius: 10px;
        padding: 10px;
    }

    [data-testid="stExpander"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "profile_created" not in st.session_state:
    st.session_state.profile_created = False

if "learner_profile" not in st.session_state:
    st.session_state.learner_profile = {}

if "completed_skills" not in st.session_state:
    st.session_state.completed_skills = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []


# =========================================================
# LOGIN / CREATE ACCOUNT SCREEN
# =========================================================

if not st.session_state.logged_in:

    st.title(
        "🎓 AI Personalized Learning Assistant"
    )

    st.write(
        "Your personalized learning journey starts here."
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account"
        ]
    )


    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader(
            "🔐 Welcome Back"
        )

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            if (
                not login_username.strip()
                or not login_password
            ):

                st.warning(
                    "Please enter your username and password."
                )

            else:

                user = login_user(
                    login_username,
                    login_password
                )


                if user is None:

                    st.error(
                        "❌ Invalid username or password."
                    )

                else:

                    st.session_state.logged_in = True

                    st.session_state.user_id = (
                        user["user_id"]
                    )


                    # -------------------------------------
                    # Restore profile
                    # -------------------------------------

                    saved_skills = get_completed_skills(
                        user["user_id"]
                    )

                    saved_courses = get_completed_courses(
                        user["user_id"]
                    )

                    saved_feedback = get_user_feedback(
                        user["user_id"]
                    )


                    interest_list = [

                        item.strip()

                        for item in user["interests"].split(",")

                        if item.strip()

                    ]


                    st.session_state.learner_profile = {

                        "user_id":
                            user["user_id"],

                        "username":
                            user["username"],

                        "name":
                            user["name"],

                        "goal":
                            user["goal"],

                        "experience":
                            user["experience"],

                        "skills":
                            saved_skills,

                        "completed_courses":
                            ", ".join(saved_courses),

                        "interests":
                            interest_list,

                        "learning_preference":
                            user["learning_preference"]

                    }


                    st.session_state.completed_skills = (
                        saved_skills
                    )


                    st.session_state.feedback = (
                        saved_feedback
                    )


                    st.session_state.profile_created = (
                        bool(user["goal"])
                    )


                    st.success(
                        f"Welcome back, {user['name']}! 🎉"
                    )


                    st.rerun()


    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    with register_tab:

        st.subheader(
            "📝 Create Your Learner Account"
        )

        new_username = st.text_input(
            "Choose a Username",
            key="register_username"
        )

        new_password = st.text_input(
            "Choose a Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        new_name = st.text_input(
            "Your Name",
            key="register_name"
        )


        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):

            if (
                not new_username.strip()
                or not new_password
                or not new_name.strip()
            ):

                st.warning(
                    "Please fill in username, password and name."
                )

            elif new_password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            elif len(new_password) < 4:

                st.warning(
                    "Password should contain at least 4 characters."
                )

            else:

                user_id = create_user(

                    new_username,

                    new_password,

                    new_name

                )


                if user_id is None:

                    st.error(
                        "❌ Username already exists. "
                        "Please choose another username."
                    )

                else:

                    st.success(
                        "🎉 Account created successfully!"
                    )

                    st.info(
                        "Go to the Login tab and log in "
                        "with your new account."
                    )


    st.stop()


# =========================================================
# LOGGED-IN USER HEADER
# =========================================================

profile = st.session_state.learner_profile

header_col1, header_col2 = st.columns(
    [5, 1]
)

with header_col1:

    st.title(
        "🎓 AI-Powered Personalized Learning Assistant"
    )

    st.caption(
        f"Welcome, **{profile['name']}** 👋"
    )

with header_col2:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.profile_created = False

        st.session_state.learner_profile = {}

        st.session_state.completed_skills = []

        st.session_state.feedback = []

        st.rerun()


st.write(
    "An AI-driven learning assistant that analyzes your "
    "goals, skills, interests and experience to create "
    "a personalized learning journey."
)

st.caption(
    "🧠 Skill Gap Analysis  •  "
    "🤖 AI Recommendations  •  "
    "🗺️ Learning Roadmap  •  "
    "📊 Progress Analytics"
)


# =========================================================
# TABS
# =========================================================

(
    tab_profile,
    tab_skills,
    tab_recommend,
    tab_path,
    tab_progress,
    tab_assistant
) = st.tabs(
    [
        "👤 Profile",
        "🧠 Skill Analysis",
        "🤖 Recommendations",
        "🗺️ Learning Path",
        "📊 Progress",
        "💬 AI Assistant"
    ]
)


# =========================================================
# TAB 1 - PROFILE
# =========================================================

with tab_profile:

    st.header(
        "👤 Learner Profile"
    )

    st.write(
        "Update your learning goals, skills and preferences."
    )


    current_profile = st.session_state.learner_profile


    name = st.text_input(
        "Your Name",
        value=current_profile.get(
            "name",
            ""
        )
    )


    goal = st.text_area(
        "🎯 What is your learning/career goal?",
        value=current_profile.get(
            "goal",
            ""
        ),
        placeholder="Example: I want to become a Data Scientist"
    )


    experience_options = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]


    current_experience = current_profile.get(
        "experience",
        "Beginner"
    )


    if current_experience not in experience_options:

        current_experience = "Beginner"


    experience = st.selectbox(
        "📈 What is your current experience level?",
        experience_options,
        index=experience_options.index(
            current_experience
        )
    )


    existing_skills = st.text_input(
        "🧠 What skills do you already know?",
        value=", ".join(
            current_profile.get(
                "skills",
                []
            )
        ),
        placeholder="Example: Python, HTML, SQL"
    )


    existing_courses = st.text_input(
        "📚 What courses have you already completed?",
        value=current_profile.get(
            "completed_courses",
            ""
        ),
        placeholder="Example: Python Basics, SQL Fundamentals"
    )


    existing_interests = st.text_input(
        "⭐ What are your interests?",
        value=", ".join(
            current_profile.get(
                "interests",
                []
            )
        ),
        placeholder="Example: AI, Data Science"
    )


    preference_options = [
        "Video Courses",
        "Reading",
        "Hands-on Projects",
        "Practice / Quizzes",
        "Mixed"
    ]


    current_preference = current_profile.get(
        "learning_preference",
        "Mixed"
    )


    if current_preference not in preference_options:

        current_preference = "Mixed"


    learning_preference = st.selectbox(
        "📚 How do you prefer to learn?",
        preference_options,
        index=preference_options.index(
            current_preference
        )
    )


    st.divider()


    if st.button(
        "💾 Save Profile",
        use_container_width=True
    ):

        if not name.strip() or not goal.strip():

            st.warning(
                "Please enter your name and learning goal."
            )

        else:

            skill_list = [

                skill.strip()

                for skill in existing_skills.split(",")

                if skill.strip()

            ]


            interest_list = [

                interest.strip()

                for interest in existing_interests.split(",")

                if interest.strip()

            ]


            course_list = [

                course.strip()

                for course in existing_courses.split(",")

                if course.strip()

            ]


            # ---------------------------------------------
            # Save profile
            # ---------------------------------------------

            update_user_profile(

                st.session_state.user_id,

                name,

                goal,

                experience,

                learning_preference,

                ",".join(interest_list)

            )


            # ---------------------------------------------
            # Save skills
            # ---------------------------------------------

            for skill in skill_list:

                save_user_skill(

                    st.session_state.user_id,

                    skill

                )


            # ---------------------------------------------
            # Save completed courses
            # ---------------------------------------------

            for course in course_list:

                save_completed_course(

                    st.session_state.user_id,

                    course

                )


            # ---------------------------------------------
            # Reload persistent data
            # ---------------------------------------------

            saved_skills = get_completed_skills(
                st.session_state.user_id
            )

            saved_courses = get_completed_courses(
                st.session_state.user_id
            )


            st.session_state.learner_profile = {

                "user_id":
                    st.session_state.user_id,

                "username":
                    current_profile.get(
                        "username",
                        ""
                    ),

                "name":
                    name.strip(),

                "goal":
                    goal.strip(),

                "experience":
                    experience,

                "skills":
                    saved_skills,

                "completed_courses":
                    ", ".join(saved_courses),

                "interests":
                    interest_list,

                "learning_preference":
                    learning_preference

            }


            st.session_state.profile_created = True


            st.success(
                "✅ Profile saved successfully!"
            )


            st.rerun()


    # -----------------------------------------------------
    # SAVED PROFILE
    # -----------------------------------------------------

    if st.session_state.profile_created:

        profile = st.session_state.learner_profile

        st.divider()

        st.subheader(
            "📋 Saved Learner Profile"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Name:**",
                profile["name"]
            )

            st.write(
                "**Goal:**",
                profile["goal"]
            )

            st.write(
                "**Experience:**",
                profile["experience"]
            )

        with col2:

            st.write(
                "**Skills:**",
                ", ".join(
                    profile["skills"]
                )
                if profile["skills"]
                else "None"
            )

            st.write(
                "**Completed Courses:**",
                profile["completed_courses"]
                if profile["completed_courses"]
                else "None"
            )

            st.write(
                "**Interests:**",
                ", ".join(
                    profile["interests"]
                )
                if profile["interests"]
                else "None"
            )

            st.write(
                "**Learning Preference:**",
                profile["learning_preference"]
            )


# =========================================================
# MAIN APPLICATION LOGIC
# =========================================================

if st.session_state.profile_created:

    profile = st.session_state.learner_profile

    learner_goal = profile["goal"]

    learner_experience = profile["experience"]

    learner_skills = profile["skills"]

    learner_interests = profile["interests"]

    learner_preference = profile["learning_preference"]


    # =====================================================
    # SKILL GAP ANALYSIS
    # =====================================================

    normalized_skills = [

        skill.lower().strip()

        for skill in learner_skills

    ]


    matched_goal, known_skills, missing_skills = (
    analyze_skill_gap(
        learner_goal,
        normalized_skills,
        st.session_state.completed_skills
    )
)


    # =====================================================
    # LEARNING PATH
    # =====================================================

    if matched_goal:

        learning_path = generate_learning_path(

            missing_skills,

            known_skills,

            matched_goal

        )

    else:

        learning_path = []


    # =====================================================
    # TAB 2 - SKILL ANALYSIS
    # =====================================================

    with tab_skills:

        st.header(
            "🧠 Skill Gap Analysis"
        )

        if matched_goal:

            st.success(
                f"🎯 Target Role: **{matched_goal}**"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "✅ Skills You Already Know"
                )

                if known_skills:

                    for skill in known_skills:

                        st.success(skill)

                else:

                    st.info(
                        "No matching skills found."
                    )

            with col2:

                st.subheader(
                    "⚠️ Skills You Need"
                )

                if missing_skills:

                    for skill in missing_skills:

                        st.warning(skill)

                else:

                    st.success(
                        "🎉 You already have all required skills!"
                    )

        else:

            st.warning(
                "We couldn't identify a supported career goal."
            )

            st.info(
                "Try AI Engineer, Data Scientist, "
                "Web Developer, or Software Developer."
            )


    # =====================================================
    # TAB 3 - RECOMMENDATIONS
    # =====================================================

    with tab_recommend:

        st.header(
            "🤖 AI-Powered Recommendations"
        )

        if matched_goal and missing_skills:

            ai_recommendations = (
                get_ai_recommendations(

                    learner_goal,

                    ", ".join(
                        learner_interests
                    ),

                    missing_skills,

                    learner_experience,

                    learner_preference,

                    st.session_state.feedback

                )
            )


            if ai_recommendations:

                st.write(
                    "Courses are ranked using your goal, "
                    "interests, skill gaps, experience, "
                    "learning preference and feedback."
                )


                for index, course in enumerate(
                    ai_recommendations,
                    start=1
                ):

                    with st.expander(
                        f"#{index} {course['title']}"
                    ):

                        st.write(
                            f"**🎯 Skill:** "
                            f"{course['skill']}"
                        )

                        st.write(
                            f"**📈 Level:** "
                            f"{course['level']}"
                        )

                        st.write(
                            f"**⏱️ Duration:** "
                            f"{course['duration']}"
                        )

                        st.write(
                            f"**📖 Description:** "
                            f"{course['description']}"
                        )

                        st.write(
                            f"🤖 AI Similarity Score: "
                            f"{course['similarity']:.2f}"
                        )


                        with st.expander(
                            "🧠 Why was this recommended?"
                        ):

                            if course["skill_match"] == 1:

                                st.success(
                                    "✅ Matches one of your "
                                    "identified skill gaps."
                                )

                            else:

                                st.info(
                                    "ℹ️ Related to your learning goal."
                                )


                            if course["experience_match"] == 1:

                                st.success(
                                    "✅ Matches your experience level."
                                )

                            else:

                                st.info(
                                    "ℹ️ Different difficulty level "
                                    "from your current experience."
                                )


                            st.write(
                                f"🔹 Profile Similarity: "
                                f"{course['similarity_score']:.2f}"
                            )

                            st.write(
                                f"🔹 Skill Gap Score: "
                                f"+{course['skill_gap_score']:.2f}"
                            )

                            st.write(
                                f"🔹 Experience Score: "
                                f"+{course['experience_score']:.2f}"
                            )

                            st.write(
                                f"🔹 Feedback Score: "
                                f"{course['feedback_score']:+.2f}"
                            )

                            st.metric(
                                "⭐ Final Recommendation Score",
                                f"{course['final_score']:.2f}"
                            )


                        if course.get("url"):

                            st.markdown(
                                f"🔗 **[Open Learning "
                                f"Resource →]({course['url']})**"
                            )


                        if course["skill"] in missing_skills:

                            st.success(
                                f"💡 Recommended because "
                                f"**{course['skill']}** is a "
                                f"skill gap for your "
                                f"**{matched_goal}** goal."
                            )


                        st.divider()

                        st.write(
                            "### 💭 Rate This Recommendation"
                        )


                        feedback_value = st.radio(

                            "Was this recommendation useful?",

                            [
                                "👍 Useful",
                                "👎 Not Useful"
                            ],

                            key=f"feedback_choice_{index}"

                        )


                        feedback_type = (

                            "Useful"

                            if feedback_value
                            == "👍 Useful"

                            else "Not Useful"

                        )


                        difficulty = st.selectbox(

                            "How difficult was this resource?",

                            [
                                "Easy",
                                "Moderate",
                                "Difficult"
                            ],

                            key=f"difficulty_{index}"

                        )


                        if st.button(

                            "💾 Submit Feedback",

                            key=f"submit_feedback_{index}"

                        ):

                            # Session feedback
                            st.session_state.feedback = (
                                save_feedback(

                                    st.session_state.feedback,

                                    course["title"],

                                    feedback_type,

                                    difficulty

                                )
                            )


                            # Persistent feedback
                            save_user_feedback(

                                st.session_state.user_id,

                                course["title"],

                                feedback_type,

                                difficulty

                            )


                            st.success(
                                "✅ Your feedback has been saved!"
                            )


                if st.session_state.feedback:

                    st.divider()

                    st.subheader(
                        "💭 Feedback Summary"
                    )

                    positive, negative = (
                        get_feedback_summary(
                            st.session_state.feedback
                        )
                    )

                    easy, moderate, difficult = (
                        get_difficulty_summary(
                            st.session_state.feedback
                        )
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "👍 Useful",
                            positive
                        )

                    with col2:

                        st.metric(
                            "👎 Not Useful",
                            negative
                        )

                    st.write(
                        "### 📊 Difficulty"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "🟢 Easy",
                            easy
                        )

                    with col2:

                        st.metric(
                            "🟡 Moderate",
                            moderate
                        )

                    with col3:

                        st.metric(
                            "🔴 Difficult",
                            difficult
                        )

            else:

                st.info(
                    "No suitable recommendations found."
                )

        elif matched_goal:

            st.success(
                "🎉 No skill gaps were identified."
            )

        else:

            st.warning(
                "Create your learner profile first."
            )


    # =====================================================
    # TAB 4 - LEARNING PATH
    # =====================================================

    with tab_path:

        st.header(
            "🗺️ Personalized Learning Path"
        )

        if matched_goal and learning_path:

            st.write(
                "Your roadmap is organized according "
                "to the prerequisites for your selected career."
            )


            for index, skill in enumerate(
                learning_path,
                start=1
            ):

                st.info(
                    f"📘 Step {index}: **{skill}**"
                )


            st.divider()

            st.subheader(
                "🛠️ Recommended Projects"
            )


            for skill in learning_path:

                project = get_project_recommendation(
                    skill
                )


                if project:

                    with st.expander(
                        f"🛠️ {skill} — "
                        f"{project['title']}"
                    ):

                        st.write(
                            f"**Project:** "
                            f"{project['title']}"
                        )

                        st.write(
                            f"**Description:** "
                            f"{project['description']}"
                        )

                        st.info(
                            f"💡 Build this project after "
                            f"learning **{skill}**."
                        )


            st.divider()

            st.subheader(
                "🏆 Learning Milestones"
            )


            total_steps = len(
                learning_path
            )


            for index, skill in enumerate(
                learning_path,
                start=1
            ):

                st.write(
                    f"Milestone {index}/{total_steps}: "
                    f"Complete **{skill}**"
                )


        elif matched_goal:

            st.success(
                "🎉 Your current profile has no missing skills."
            )

        else:

            st.warning(
                "Create a valid learner profile first."
            )


    # =====================================================
    # TAB 5 - PROGRESS
    # =====================================================

    with tab_progress:

        st.header(
            "📊 Progress & Learning Analytics"
        )

        if matched_goal and learning_path:


            def get_prerequisite(
                skill,
                goal_name
            ):
                """Get prerequisite for selected career."""

                try:

                    skill_data = pd.read_csv(
                        "data/skills.csv",
                        keep_default_na=False
                    )


                    rows = skill_data[

                        (
                            skill_data["goal"]
                            .astype(str)
                            .str.strip()
                            .str.lower()

                            == goal_name
                            .strip()
                            .lower()
                        )

                        &

                        (
                            skill_data["skill"]
                            .astype(str)
                            .str.strip()
                            .str.lower()

                            == skill
                            .strip()
                            .lower()
                        )

                    ]


                    if rows.empty:

                        return None


                    prerequisite = str(
                        rows.iloc[0]["prerequisite"]
                    ).strip()


                    if (
                        not prerequisite
                        or prerequisite.lower()
                        == "none"
                    ):

                        return None


                    return prerequisite


                except Exception:

                    return None


            st.subheader(
                "✅ Update Your Skill Progress"
            )


            for skill in learning_path:

                prerequisite = get_prerequisite(
                    skill,
                    matched_goal
                )


                prerequisite_completed = (

                    prerequisite is None

                    or prerequisite.lower()
                    in {
                        x.lower()
                        for x in known_skills
                    }

                    or prerequisite.lower()
                    in {
                        x.lower()
                        for x in st.session_state.completed_skills
                    }

                )


                currently_completed = (

                    skill.lower()

                    in {
                        x.lower()
                        for x in st.session_state.completed_skills
                    }

                )


                if not prerequisite_completed:

                    st.checkbox(

                        f"🔒 {skill} — Complete "
                        f"{prerequisite} first",

                        value=False,

                        disabled=True,

                        key=f"progress_{skill}"

                    )

                else:

                    st.checkbox(

                        skill,

                        value=currently_completed,

                        key=f"progress_{skill}"

                    )


            # ---------------------------------------------
            # READ COMPLETED SKILLS
            # ---------------------------------------------

            current_path_completed = []


            for skill in learning_path:

                key = f"progress_{skill}"


                if st.session_state.get(
                    key,
                    False
                ):

                    current_path_completed.append(
                        skill
                    )


            # ---------------------------------------------
            # Preserve previous skills
            # ---------------------------------------------

            persistent_skills = [

                skill

                for skill in st.session_state.completed_skills

                if skill not in learning_path

            ]


            st.session_state.completed_skills = (

                persistent_skills
                + current_path_completed

            )


            # ---------------------------------------------
            # Save newly completed skills
            # ---------------------------------------------

            for skill in current_path_completed:

                save_user_skill(

                    st.session_state.user_id,

                    skill

                )


            progress = calculate_progress(

                learning_path,

                current_path_completed

            )


            next_skill = get_next_skill(

                learning_path,

                current_path_completed

            )


            completed_count = len(
                current_path_completed
            )


            total_count = len(
                learning_path
            )


            remaining_count = (

                total_count
                - completed_count

            )


            progress_percentage = (
                progress * 100
            )


            st.divider()


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "📈 Progress",
                    f"{progress_percentage:.0f}%"
                )


            with col2:

                st.metric(
                    "✅ Completed",
                    completed_count
                )


            with col3:

                st.metric(
                    "📚 Remaining",
                    remaining_count
                )


            with col4:

                st.metric(
                    "🎯 Current Focus",
                    next_skill
                    if next_skill
                    else "Completed!"
                )


            st.progress(
                progress
            )


            st.divider()

            st.subheader(
                "🧠 Skill Status"
            )


            for skill in learning_path:

                if skill in current_path_completed:

                    st.success(
                        f"✅ {skill} — Completed"
                    )

                elif skill == next_skill:

                    st.info(
                        f"🔄 {skill} — Current Focus"
                    )

                else:

                    prerequisite = get_prerequisite(
                        skill,
                        matched_goal
                    )


                    if prerequisite:

                        st.warning(
                            f"🔒 {skill} — Complete "
                            f"{prerequisite} first"
                        )

                    else:

                        st.warning(
                            f"⏳ {skill} — Pending"
                        )


            st.divider()

            st.subheader(
                "💭 Recommendation Feedback"
            )


            positive, negative = (
                get_feedback_summary(
                    st.session_state.feedback
                )
            )


            easy, moderate, difficult = (
                get_difficulty_summary(
                    st.session_state.feedback
                )
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "👍 Useful",
                    positive
                )


            with col2:

                st.metric(
                    "👎 Not Useful",
                    negative
                )


            st.write(
                "### 📊 Resource Difficulty"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "🟢 Easy",
                    easy
                )

            with col2:

                st.metric(
                    "🟡 Moderate",
                    moderate
                )

            with col3:

                st.metric(
                    "🔴 Difficult",
                    difficult
                )


        elif matched_goal:

            st.success(
                "🎉 Your current profile has no missing skills."
            )

        else:

            st.warning(
                "Create a valid learner profile first."
            )


    # =====================================================
    # TAB 6 - AI ASSISTANT
    # =====================================================

    with tab_assistant:

        st.header(
            "💬 AI Learning Assistant"
        )

        st.write(
            "Ask questions about your skills, "
            "learning path, recommendations or progress."
        )


        if matched_goal:

            question = st.text_input(
                "💬 Ask a question",
                placeholder=(
                    "Example: What should I learn next?"
                )
            )


            if st.button(
                "💡 Ask Assistant",
                use_container_width=True
            ):

                if question.strip():

                    response = get_assistant_response(

                        question,

                        profile,

                        known_skills,

                        missing_skills,

                        learning_path,

                        st.session_state.completed_skills

                    )

                    st.markdown(
                        response
                    )

                else:

                    st.warning(
                        "Please enter a question."
                    )


            st.divider()

            st.subheader(
                "💡 Example Questions"
            )

            st.write(
                "• What should I learn next?"
            )

            st.write(
                "• What skills am I missing?"
            )

            st.write(
                "• What skills do I already know?"
            )

            st.write(
                "• What is my progress?"
            )

            st.write(
                "• Why do I need Machine Learning?"
            )

            st.write(
                "• Can I skip Deep Learning?"
            )

            st.write(
                "• Can I do Model Deployment before Deep Learning?"
            )

        else:

            st.info(
                "Please create your learner profile first."
            )