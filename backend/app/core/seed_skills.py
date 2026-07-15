"""
Seeds the `skills` table from the controlled vocabulary in
app.parser.skill_data. Safe to re-run (skips names that already exist).

Usage:
    python -m app.core.seed_skills
"""
from app.core.database import SessionLocal
from app.models.skill import Skill
from app.parser.skill_data import all_canonical_skills


def seed_skills():
    db = SessionLocal()
    try:
        existing = {row.name for row in db.query(Skill.name).all()}
        new_skills = [Skill(name=name) for name in all_canonical_skills() if name not in existing]
        if new_skills:
            db.add_all(new_skills)
            db.commit()
        print(f"Seeded {len(new_skills)} new skills ({len(existing)} already present).")
    finally:
        db.close()


if __name__ == "__main__":
    seed_skills()
