"""
Top-level resume parsing orchestrator. Given a saved resume file, runs
the full pipeline: text extraction -> contact info -> sections ->
skills/education/experience/projects/certifications, and returns a dict
shaped for app.schemas.resume.ResumeCreate.
"""
from app.parser.text_extractor import extract_text
from app.parser.contact_extractor import extract_name, extract_email, extract_phone
from app.parser.section_extractor import split_into_sections
from app.parser.skill_extractor import extract_skills
from app.parser.structured_parser import (
    parse_education,
    parse_experience,
    parse_projects,
    parse_certifications,
)


def parse_resume(file_path: str, file_extension: str) -> dict:
    raw_text = extract_text(file_path, file_extension)

    if not raw_text.strip():
        # Still return a valid (mostly empty) structure rather than raising —
        # the resume can be stored and the user notified to check the file,
        # rather than the whole upload failing.
        return {
            "name": None,
            "email": None,
            "phone": None,
            "education": [],
            "experience": [],
            "projects": [],
            "skills": [],
            "certifications": [],
            "raw_text": "",
        }

    sections = split_into_sections(raw_text)

    # Skills: search the dedicated Skills section if present, but also the
    # full document, since many resumes scatter skills into project/experience
    # bullet points as well.
    skills_from_section = extract_skills(sections.get("skills", ""))
    skills_from_full_text = extract_skills(raw_text)
    skills = sorted(set(skills_from_section) | set(skills_from_full_text))

    return {
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "education": parse_education(sections.get("education", "")),
        "experience": parse_experience(sections.get("experience", "")),
        "projects": parse_projects(sections.get("projects", "")),
        "skills": skills,
        "certifications": parse_certifications(sections.get("certifications", "")),
        "raw_text": raw_text,
    }
