import pandas as pd
import networkx as nx


def load_skill_data():
    """Load skill and prerequisite data."""

    return pd.read_csv(
        "data/skills.csv",
        keep_default_na=False
    )


def generate_learning_path(
    missing_skills,
    known_skills=None,
    goal=None
):
    """
    Generate an ordered learning path based on
    prerequisites for the selected career goal.

    The prerequisite graph is built only from
    the selected goal so that skills shared by
    multiple careers do not create incorrect
    cross-career dependencies.
    """

    skill_data = load_skill_data()

    if known_skills is None:
        known_skills = []


    # =====================================================
    # NORMALIZE KNOWN SKILLS
    # =====================================================

    known = {
        str(skill).strip().lower()
        for skill in known_skills
        if str(skill).strip()
    }


    # =====================================================
    # FILTER DATA BY CAREER GOAL
    # =====================================================

    if goal:

        goal_name = str(goal).strip().lower()

        skill_data = skill_data[
            skill_data["goal"]
            .astype(str)
            .str.strip()
            .str.lower()
            == goal_name
        ]


    if skill_data.empty:

        return []


    # =====================================================
    # CREATE GRAPH
    # =====================================================

    graph = nx.DiGraph()


    # =====================================================
    # BUILD PREREQUISITE GRAPH
    # =====================================================

    for _, row in skill_data.iterrows():

        skill = str(
            row["skill"]
        ).strip()

        prerequisite = str(
            row["prerequisite"]
        ).strip()


        if not skill:

            continue


        graph.add_node(
            skill
        )


        if (
            prerequisite
            and prerequisite.lower() != "none"
        ):

            graph.add_edge(
                prerequisite,
                skill
            )


    # =====================================================
    # START WITH MISSING SKILLS
    # =====================================================

    relevant_skills = {

        str(skill).strip()

        for skill in missing_skills

        if str(skill).strip()

        and str(skill).strip().lower()
        not in known

    }


    # =====================================================
    # ADD REQUIRED PREREQUISITES
    # =====================================================

    changed = True


    while changed:

        changed = False


        for skill in list(
            relevant_skills
        ):

            if skill not in graph:

                continue


            prerequisites = list(
                graph.predecessors(skill)
            )


            for prerequisite in prerequisites:

                # Do not add skills already known
                if prerequisite.lower() in known:

                    continue


                if prerequisite not in relevant_skills:

                    relevant_skills.add(
                        prerequisite
                    )

                    changed = True


    # =====================================================
    # CREATE RELEVANT SUBGRAPH
    # =====================================================

    subgraph = graph.subgraph(
        relevant_skills
    ).copy()


    # =====================================================
    # TOPOLOGICAL SORT
    # =====================================================

    try:

        ordered_skills = list(
            nx.topological_sort(
                subgraph
            )
        )

    except nx.NetworkXUnfeasible:

        ordered_skills = list(
            relevant_skills
        )


    # =====================================================
    # REMOVE KNOWN SKILLS
    # =====================================================

    ordered_skills = [

        skill

        for skill in ordered_skills

        if skill.lower() not in known

    ]


    return ordered_skills