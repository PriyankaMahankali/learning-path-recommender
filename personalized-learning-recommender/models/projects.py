def get_project_recommendation(skill):
    """
    Return a practical project recommendation
    based on the learner's skill gap.
    """

    projects = {

        "Python": {
            "title": "Student Grade Analysis System",
            "description": (
                "Build a Python application that reads student "
                "marks, calculates grades and generates a "
                "performance report."
            )
        },

        "Statistics": {
            "title": "Student Performance Statistical Analysis",
            "description": (
                "Analyze a student performance dataset using "
                "mean, median, standard deviation and correlation."
            )
        },

        "SQL": {
            "title": "Student Database Management System",
            "description": (
                "Design a relational database for students, "
                "courses and marks and create SQL queries "
                "for analysis."
            )
        },

        "Pandas": {
            "title": "Data Cleaning and Analysis Project",
            "description": (
                "Use Pandas to clean a real-world dataset, "
                "handle missing values and generate useful "
                "statistics."
            )
        },

        "NumPy": {
            "title": "Numerical Data Processing System",
            "description": (
                "Build a numerical analysis application using "
                "NumPy arrays and mathematical operations."
            )
        },

        "Data Visualization": {
            "title": "Interactive Data Visualization Dashboard",
            "description": (
                "Create visualizations that communicate trends "
                "and patterns in a dataset."
            )
        },

        "Mathematics": {
            "title": "Mathematics for Machine Learning Toolkit",
            "description": (
                "Build a small Python toolkit demonstrating "
                "vectors, matrices, probability and mathematical "
                "operations used in AI."
            )
        },

        "Machine Learning": {
            "title": "Student Performance Prediction System",
            "description": (
                "Build a machine learning model that predicts "
                "student performance using relevant features."
            )
        },

        "Deep Learning": {
            "title": "Image Classification System",
            "description": (
                "Build a neural-network-based image classification "
                "system using a suitable image dataset."
            )
        },

        "Neural Networks": {
            "title": "Neural Network Classification Project",
            "description": (
                "Implement and train a neural network to classify "
                "data and evaluate its performance."
            )
        },

        "Model Deployment": {
            "title": "Machine Learning Model Deployment",
            "description": (
                "Deploy a trained machine learning model through "
                "a simple web API."
            )
        },

        "MLOps": {
            "title": "Machine Learning Model Lifecycle Project",
            "description": (
                "Create a basic ML pipeline covering model "
                "training, tracking and deployment."
            )
        },

        "HTML": {
            "title": "Personal Portfolio Website",
            "description": (
                "Build a responsive personal portfolio website "
                "using HTML."
            )
        },

        "CSS": {
            "title": "Responsive Portfolio Website",
            "description": (
                "Design a responsive portfolio interface using "
                "modern CSS techniques."
            )
        },

        "JavaScript": {
            "title": "Interactive Web Application",
            "description": (
                "Build an interactive browser application using "
                "JavaScript."
            )
        },

        "Git": {
            "title": "Version-Controlled Software Project",
            "description": (
                "Create a software project and manage its "
                "development history using Git and GitHub."
            )
        },

        "React": {
            "title": "React Learning Dashboard",
            "description": (
                "Build a responsive learning dashboard using "
                "React components and state management."
            )
        },

        "Backend Development": {
            "title": "Learning Management Backend",
            "description": (
                "Build a backend service that manages users, "
                "courses and learning progress."
            )
        },

        "Database": {
            "title": "Learning Management Database",
            "description": (
                "Design a database for learners, courses, "
                "skills and progress tracking."
            )
        },

        "Programming": {
            "title": "Console-Based Problem Solving Application",
            "description": (
                "Build a programming application that demonstrates "
                "variables, conditions, loops, functions and "
                "problem-solving techniques."
            )
        },

        "Data Structures": {
            "title": "Data Structures Demonstration System",
            "description": (
                "Implement common data structures and demonstrate "
                "their operations through a simple application."
            )
        },

        "Algorithms": {
            "title": "Algorithm Visualization Project",
            "description": (
                "Build an application that demonstrates sorting "
                "and searching algorithms."
            )
        },

        "Software Testing": {
            "title": "Automated Testing Project",
            "description": (
                "Create a small application with unit tests and "
                "automated test cases."
            )
        }
    }

    return projects.get(skill)