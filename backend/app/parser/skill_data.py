"""
Master skill vocabulary used for extraction and matching.

Per the project spec: skill extraction must NOT use AI — this is a
controlled vocabulary matched against resume/JD text via word-boundary
regex. Aliases map common variants to a single canonical name (e.g.
"ReactJS" / "React.js" -> "React") so matching stays consistent between
a resume and a job description that spell things differently.

This list seeds the `skills` DB table (see app/core/seed_skills.py) and
is also imported directly by the parser/matcher for fast in-memory use.
"""

# canonical_name -> [aliases...] (canonical name itself is always matched too)
SKILL_ALIASES: dict[str, list[str]] = {
    "Python": ["python3"],
    "Java": [],
    "JavaScript": ["js", "javascript(es6)", "es6"],
    "TypeScript": ["ts"],
    "C++": ["cpp"],
    "C#": ["csharp"],
    "Go": ["golang"],
    "React": ["reactjs", "react.js"],
    "Node": ["nodejs", "node.js"],
    "Angular": ["angularjs"],
    "Vue": ["vuejs", "vue.js"],
    "Django": [],
    "Flask": [],
    "FastAPI": [],
    "Spring Boot": ["springboot", "spring"],
    "MongoDB": ["mongo"],
    "PostgreSQL": ["postgres", "psql"],
    "MySQL": [],
    "SQL": [],
    "Redis": [],
    "Docker": [],
    "Kubernetes": ["k8s"],
    "AWS": ["amazon web services"],
    "Azure": [],
    "GCP": ["google cloud", "google cloud platform"],
    "Git": [],
    "GitHub": [],
    "CI/CD": ["ci cd", "continuous integration"],
    "Linux": [],
    "HTML": ["html5"],
    "CSS": ["css3"],
    "Tailwind CSS": ["tailwind", "tailwindcss"],
    "REST API": ["rest apis", "restful api", "restful apis"],
    "GraphQL": [],
    "Machine Learning": ["ml"],
    "Deep Learning": ["dl"],
    "TensorFlow": [],
    "PyTorch": [],
    "Pandas": [],
    "NumPy": [],
    "scikit-learn": ["sklearn"],
    "NLP": ["natural language processing"],
    "Data Analysis": [],
    "Power BI": ["powerbi"],
    "Excel": ["ms excel", "microsoft excel"],
    "Agile": ["scrum"],
    "Jira": [],
}


def all_canonical_skills() -> list[str]:
    return list(SKILL_ALIASES.keys())
