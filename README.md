# 🎓 AI-Powered Personalized Learning Path Recommender

An AI-powered personalized learning assistant that analyzes a learner's
career goals, existing skills, interests, experience level and learning
preferences to generate a customized learning journey.

The system identifies skill gaps, recommends relevant learning resources,
generates prerequisite-based learning paths, tracks progress, learns from
feedback and provides an AI learning assistant for learner queries.

---

## 📌 Problem Statement

Online learning platforms provide thousands of courses, but learners often
struggle to determine:

- What they should learn
- Which skills they are missing
- Which course should be taken first
- What prerequisites are required
- How their progress should be tracked
- Which resources are most relevant to their career goal

A one-size-fits-all learning approach does not work effectively because
learners have different skill levels, interests, goals and learning
preferences.

This project addresses this problem by creating an AI-powered personalized
learning assistant that converts learner information into a structured and
adaptive learning roadmap.

---

## 🎯 Objectives

The main objectives of the project are:

1. Create a personalized learner profile.
2. Understand the learner's career goal using natural language.
3. Identify the learner's existing and missing skills.
4. Recommend relevant learning resources using AI/ML techniques.
5. Generate a prerequisite-based learning path.
6. Recommend projects associated with required skills.
7. Track learner progress and milestones.
8. Adapt recommendations based on learner feedback.
9. Provide an AI learning assistant for personalized guidance.
10. Store learner history for continuous personalization across career goals.

---

## ✨ Key Features

### 👤 1. Learner Profiling

The system collects:

- Name
- Career/learning goal
- Experience level
- Existing skills
- Completed courses
- Interests
- Learning preference

The learner can describe their goal using natural language.

Example:

> I want to become a Data Scientist

---

### 🧠 2. Skill Gap Analysis

The system compares the learner's existing skills with the skills
required for the selected career.

Example:

```text
Target Role: Data Scientist

Already Known:
✅ Python
✅ SQL

Skills Needed:
⚠️ Statistics
⚠️ Pandas
⚠️ NumPy
⚠️ Data Visualization
⚠️ Machine Learning
