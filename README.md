# 🎓 AI-Powered Personalized Learning Path Recommender

This allows the system to focus the learning journey on skills that the
learner actually needs.

---

## 🤖 3. AI-Based Course Recommendation

The recommendation engine uses:

* TF-IDF vectorization
* Cosine similarity
* Skill-gap matching
* Experience-level matching
* Learner feedback

A personalized learner profile is converted into a text representation and
compared with course descriptions.

The final recommendation score combines multiple factors:

```text
Final Score =
    Profile Similarity Score
  + Skill Gap Score
  + Experience Score
  + Feedback Score
```

This produces a ranked list of personalized learning resources.

---

## 🧩 4. Career-Specific Recommendations

Recommendations are restricted to skills relevant to the learner's selected
career goal.

Supported career paths include:

* 🤖 AI Engineer
* 📊 Data Scientist
* 🌐 Web Developer
* 💻 Software Developer

This prevents unrelated courses from dominating the recommendations.

---

## 🗺️ 5. Prerequisite-Based Learning Path

The system uses a prerequisite graph to determine the correct order of
learning.

Example:

```text
Python
   ↓
Pandas
   ↓
Data Visualization
```

Another example:

```text
Statistics
     ↓
Machine Learning
     ↓
Deep Learning
```

The prerequisite relationships are represented as a directed graph and
topological ordering is used to generate the learning sequence.

---

## 🛠️ 6. Project Recommendations

The system recommends practical projects related to the skills in the
learner's learning path.

This helps learners move from theoretical learning to hands-on practice.

---

## 📊 7. Progress Tracking

Learners can mark skills as completed.

The dashboard displays:

* Overall progress
* Completed skills
* Remaining skills
* Current focus
* Skill status
* Learning milestones

Prerequisites are also enforced.

For example:

```text
✅ Python

🔒 Pandas
   Complete Python first
```

Once Python is completed:

```text
✅ Python

☐ Pandas
```

---

## 💭 8. Feedback-Based Adaptation

Learners can provide feedback for recommended resources.

Feedback includes:

* 👍 Useful
* 👎 Not Useful
* 🟢 Easy
* 🟡 Moderate
* 🔴 Difficult

The feedback affects the recommendation score.

Example:

```text
Useful       → +2
Not Useful   → -2
Easy         → +0.5
Difficult    → -1
```

This allows recommendations to adapt to learner preferences.

---

## 💾 9. Persistent Learner History

The system uses SQLite to store learner information.

Stored information includes:

* User accounts
* Learner profiles
* Completed skills
* Completed courses
* Recommendation feedback

This allows learning history to persist after logout and application
restart.

---

## 🔄 10. Cross-Career Skill Reuse

A major personalization feature is the ability to reuse skills learned from
previous career paths.

Example:

```text
AI Engineer
     ↓
Learner completes:
Python
Statistics
Machine Learning
     ↓
Later selects:
Data Scientist
```

The system recognizes the previously completed skills.

Instead of asking the learner to repeat them:

```text
Python              ✅ Already Known
Statistics          ✅ Already Known
Machine Learning    ✅ Already Known
```

The system focuses on new skills:

```text
SQL
Pandas
NumPy
Data Visualization
Deep Learning
```

This creates a continuous learner knowledge profile.

---

## 💬 11. AI Learning Assistant

The application includes an AI learning assistant that can answer questions
about:

* Missing skills
* Current progress
* Learning path
* Recommended resources
* Prerequisites
* Next learning steps

Example questions:

```text
What should I learn next?

What skills am I missing?

What skills do I already know?

What is my progress?

Why do I need Machine Learning?

Can I skip Deep Learning?

Can I do Model Deployment before Deep Learning?
```

---

## 🧠 System Architecture

```text
                     ┌─────────────────────┐
                     │      Learner        │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Learner Profile   │
                     │ Goal / Skills /     │
                     │ Interests / Level   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  Skill Gap Analysis │
                     └──────────┬──────────┘
                                │
                     ┌──────────┴──────────┐
                     ▼                     ▼
           ┌──────────────────┐    ┌──────────────────┐
           │ Recommendation   │    │ Learning Path    │
           │ Engine           │    │ Generator        │
           │                  │    │                  │
           │ TF-IDF           │    │ Prerequisites    │
           │ Cosine Similarity│    │ Graph            │
           │ Skill Matching   │    │ Topological Sort │
           └────────┬─────────┘    └────────┬─────────┘
                    │                       │
                    └─────────────┬─────────┘
                                  ▼
                       ┌─────────────────────┐
                       │ Personalized        │
                       │ Learning Journey    │
                       └──────────┬──────────┘
                                  │
                       ┌──────────┼──────────┐
                       ▼          ▼          ▼
                 📚 Courses   🛠️ Projects  📊 Progress
                       │          │          │
                       └──────────┼──────────┘
                                  ▼
                          💭 Learner Feedback
                                  │
                                  ▼
                       🔄 Recommendation Update
                                  │
                                  ▼
                        💾 Persistent Database
```

---

## 🔬 AI/ML Methodology

### Step 1 — Learner Profile Creation

The learner provides:

* Goal
* Skills
* Experience
* Interests
* Learning Preference

### Step 2 — Skill Gap Identification

The system compares learner skills with the required skills associated with
the target career.

```text
Required Skills - Known Skills = Skill Gap
```

### Step 3 — Course Representation

Each course is represented using:

* Title
* Skill
* Level
* Description

These fields are combined into course text.

### Step 4 — TF-IDF Vectorization

TF-IDF converts learner and course text into numerical vectors based on word
importance.

### Step 5 — Cosine Similarity

Cosine similarity measures how closely the learner profile matches each
course.

Higher similarity indicates greater relevance.

### Step 6 — Personalization Score

The system combines:

* Similarity
* Skill Gap
* Experience
* Feedback

to calculate the final recommendation score.

### Step 7 — Ranking

Courses are sorted according to their final personalization score and the
highest-ranked resources are presented to the learner.

---

## 🗺️ Learning Path Generation

The learning path generator represents prerequisites using a directed graph.

Example:

```text
Programming
     ↓
Data Structures
     ↓
Algorithms
```

The graph is processed using topological sorting to produce a valid learning
sequence.

Already-known skills are excluded from the new learning path.

---

## 💾 Database

SQLite is used for persistent learner storage.

### Main tables

#### Users

Stores:

* `user_id`
* `username`
* `password`
* `name`
* `goal`
* `experience`
* `learning_preference`
* `interests`

#### User Skills

Stores:

* `user_id`
* `skill`
* `status`
* `completed_at`

#### Completed Courses

Stores:

* `user_id`
* `course`
* `completed_at`

#### Feedback

Stores:

* `user_id`
* `course`
* `feedback`
* `difficulty`
* `created_at`

---

## 🛠️ Technologies Used

| Technology   | Purpose                                         |
| ------------ | ----------------------------------------------- |
| Python       | Core programming language                       |
| Streamlit    | Web application and UI                          |
| Pandas       | Data processing                                 |
| Scikit-learn | TF-IDF and cosine similarity                    |
| NetworkX     | Prerequisite graph and learning path generation |
| SQLite       | Persistent learner database                     |
| CSV          | Course and skill datasets                       |

---

## 📁 Project Structure

```text
personalized-learning-recommender/
│
├── app.py
│
├── ai/
│   ├── ai_recommender.py
│   └── assistant.py
│
├── models/
│   ├── database.py
│   ├── skill_gap.py
│   ├── path_generator.py
│   ├── progress.py
│   ├── feedback.py
│   └── projects.py
│
├── data/
│   ├── courses.csv
│   ├── skills.csv
│   └── learning_assistant.db
│
├── README.md
│
└── ...
```

---

## ⚙️ Installation

### 1. Clone or download the project

Open a terminal in the project directory.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install streamlit pandas scikit-learn networkx
```

If a `requirements.txt` file is provided, use:

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in the browser.

---

## 🚀 How to Use

### Step 1 — Create an Account

Create a learner account using:

* Username
* Password
* Name

### Step 2 — Login

Log in using the created credentials.

### Step 3 — Create/Update Profile

Enter:

* Career Goal
* Experience Level
* Existing Skills
* Completed Courses
* Interests
* Learning Preference

### Step 4 — Analyze Skills

Open:

```text
🧠 Skill Analysis
```

to view:

* Known skills
* Missing skills
* Target career

### Step 5 — View Recommendations

Open:

```text
🤖 Recommendations
```

to view AI-ranked learning resources.

### Step 6 — Follow Learning Path

Open:

```text
🗺️ Learning Path
```

to follow the prerequisite-based roadmap.

### Step 7 — Track Progress

Open:

```text
📊 Progress
```

and mark completed skills.

### Step 8 — Give Feedback

Rate recommendations as:

* Useful / Not Useful
* Easy / Moderate / Difficult

### Step 9 — Ask the AI Assistant

Use:

```text
💬 AI Assistant
```

to ask questions about your personalized learning journey.

---

## 🧪 Supported Career Roles

The current system supports:

### 🤖 AI Engineer

Core skills include:

* Python
* Mathematics
* Statistics
* Machine Learning
* Deep Learning
* Neural Networks
* Model Deployment
* MLOps

### 📊 Data Scientist

Core skills include:

* Python
* Statistics
* SQL
* Pandas
* NumPy
* Data Visualization
* Machine Learning
* Deep Learning

### 🌐 Web Developer

Core skills include:

* HTML
* CSS
* JavaScript
* Git
* React
* Backend Development
* Database

### 💻 Software Developer

Core skills include:

* Programming
* Data Structures
* Algorithms
* Git
* Database
* Software Testing

---

## 🌟 Innovation

The project goes beyond basic course recommendation by combining several
personalization mechanisms:

* Career-specific skill gap analysis.
* Prerequisite-aware learning paths.
* Explainable recommendation scores.
* Feedback-based recommendation adaptation.
* Persistent learner history.
* Cross-career skill reuse.
* Progress-aware learning.
* AI-based learner assistance.

The cross-career skill reuse mechanism allows previously acquired skills to
remain part of the learner's long-term knowledge profile.

---

## 📊 Example Learning Scenario

A learner starts with:

```text
Goal: AI Engineer
Skills: Python
```

The system identifies missing skills and generates a learning path.

After completing several AI Engineer skills, the learner can switch to:

```text
Goal: Data Scientist
```

Previously completed skills are retained.

The system then calculates the new skill gap based on the learner's existing
knowledge instead of starting from zero.

---

## 🔐 Data Persistence

Learner information is stored locally using SQLite.

Therefore:

```text
Logout
   ↓
Close Application
   ↓
Restart Application
   ↓
Login
   ↓
Previous Learner Data Restored
```

The database stores learner history independently of Streamlit's temporary
session state.

---

## ⚠️ Limitations

The current prototype has some limitations:

* The course database is currently a curated local dataset.
* The supported career roles are predefined.
* Recommendations depend on the available course metadata.
* The AI recommendation engine currently uses classical NLP techniques
  rather than a large language model for course ranking.
* Authentication is designed for a prototype/local application.
* Production deployment would require stronger password security,
  authentication and database infrastructure.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Integration with real online learning platforms.
* Larger and continuously updated course databases.
* LLM-powered conversational recommendations.
* Semantic embeddings using transformer models.
* More career domains.
* Advanced learner analytics.
* Time-based personalized schedules.
* Difficulty prediction.
* Adaptive assessments and quizzes.
* Cloud database support.
* Secure production authentication.
* Real-time learning resource availability.
