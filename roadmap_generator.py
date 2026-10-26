
ROADMAP = {
    "Python": "Practice Python fundamentals, functions, modules, and data structures.",
    "SQL": "Learn SELECT, filtering, JOINs, GROUP BY, and subqueries.",
    "Excel": "Practice formulas, pivot tables, charts, and data cleaning.",
    "Pandas": "Learn DataFrames, filtering, grouping, merging, and missing values.",
    "Power BI": "Build dashboards and practice data modeling and DAX basics.",
    "Tableau": "Create interactive visualizations and dashboards.",
    "Statistics": "Study probability, distributions, hypothesis testing, and correlation.",
    "Machine Learning": "Learn supervised learning, model evaluation, and feature engineering.",
    "scikit-learn": "Build classification and regression models using pipelines.",
    "NumPy": "Practice arrays, vectorized operations, and numerical computing.",
    "FastAPI": "Build REST endpoints, validate inputs, and serve a small ML model.",
    "Docker": "Containerize a Python application and learn images and containers.",
    "Git": "Practice commits, branches, merges, and GitHub workflows.",
    "Deep Learning": "Study neural networks, backpropagation, and training workflows.",
    "LLM": "Learn tokenization, prompting, model limitations, and evaluation.",
    "RAG": "Build a retrieval-augmented generation prototype with document search.",
    "APIs": "Learn HTTP methods, JSON, request handling, and API testing.",
    "PyTorch": "Build tensors, neural networks, training loops, and evaluation.",
    "NLP": "Practice text preprocessing, classification, and named entity recognition.",
    "Transformers": "Study attention, tokenization, and pretrained transformer models.",
    "Hugging Face": "Load a pretrained model and run a text-classification pipeline.",
    "OpenCV": "Practice image loading, resizing, filtering, and feature extraction.",
    "CNN": "Build a basic convolutional neural network for image classification.",
    "YOLO": "Learn object detection, bounding boxes, and model evaluation.",
    "Java": "Practice object-oriented programming and core Java collections.",
    "C++": "Practice functions, classes, pointers, and standard library containers.",
    "C#": "Learn C# syntax, classes, collections, and .NET application basics.",
    "JavaScript": "Practice modern JavaScript, asynchronous code, and API requests.",
    "PostgreSQL": "Practice relational schemas, joins, indexes, and query optimization.",
    "MySQL": "Practice relational database design and SQL queries.",
    "MongoDB": "Learn document collections, queries, and aggregation pipelines.",
    "TensorFlow": "Build and train a basic neural network using Keras.",
    "Flask": "Create a small Python web application and REST endpoints.",
    "MLflow": "Track experiments, parameters, metrics, and model versions.",
    "AWS": "Learn core cloud concepts and deploy a simple application.",
    "Azure": "Learn core cloud services and deploy a simple application.",
    "Linux": "Practice shell commands, files, permissions, and process management.",
}


def generate_roadmap(missing_skills: list[str]) -> list[dict]:
    """Generate a four-week plan from the missing skills."""
    if not missing_skills:
        return [{
            "week": "Next step",
            "skills": [],
            "task": (
                "No required skills were missed by keyword matching. "
                "Build a portfolio project and practice explaining your work."
            ),
        }]

    roadmap = []
    weeks = 4

    # Distribute skills across four weeks.
    for week_index in range(weeks):
        weekly_skills = missing_skills[week_index::weeks]

        if not weekly_skills:
            continue

        tasks = [
            ROADMAP.get(
                skill,
                f"Study {skill} fundamentals and build a small practical exercise."
            )
            for skill in weekly_skills
        ]

        roadmap.append({
            "week": f"Week {week_index + 1}",
            "skills": weekly_skills,
            "task": " ".join(tasks),
        })

    return roadmap
