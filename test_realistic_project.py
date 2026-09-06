from datetime import date

from database import SessionLocal
from models import Project, Activity, Dependency


db = SessionLocal()


# =========================================================
# CREATE PROJECT
# =========================================================
project = Project(
    name="ConstructAI Realistic Building Demo"
)

db.add(project)
db.commit()
db.refresh(project)

PROJECT_ID = project.id

print(f"Project created with ID: {PROJECT_ID}")


# =========================================================
# ACTIVITIES
# =========================================================

activities_data = [

    ("A01", "Excavation", "Earthwork", 5),
    ("A02", "PCC", "Foundation", 3),

    ("A03", "Footing Reinforcement", "Structure", 5),
    ("A04", "Footing Concrete", "Structure", 2),

    ("A05", "Pedestal Reinforcement", "Structure", 3),
    ("A06", "Pedestal Concrete", "Structure", 2),

    ("A07", "Column Reinforcement", "Structure", 5),
    ("A08", "Column Concrete", "Structure", 2),

    ("A09", "Slab Reinforcement", "Structure", 6),
    ("A10", "Slab Concrete", "Structure", 2),

    ("A11", "Masonry", "Architecture", 8),
    ("A12", "Electrical & Plumbing Rough-in", "MEP", 6),

    ("A13", "Plastering", "Finishes", 7),
    ("A14", "Flooring & Ceiling", "Finishes", 8),
    ("A15", "Painting & Final Finishes", "Finishes", 6),
]


start_date = date(2026, 9, 1)

activity_objects = {}

current_day = 0


for code, name, category, duration in activities_data:

    planned_start = start_date

    planned_finish = start_date

    activity = Activity(
        project_id=PROJECT_ID,
        activity_code=code,
        name=name,
        wbs=f"1.{len(activity_objects) + 1}",
        category=category,
        unit="days",
        quantity=1,
        planned_start=planned_start,
        planned_finish=planned_finish,
        planned_duration=duration,
        progress=0
    )

    db.add(activity)

    db.flush()

    activity_objects[code] = activity


db.commit()

print("15 realistic activities created successfully.")


# =========================================================
# DEPENDENCIES
# =========================================================

dependencies = [

    # Foundation
    ("A01", "A02"),

    # Footing
    ("A02", "A03"),
    ("A03", "A04"),

    # Pedestal
    ("A04", "A05"),
    ("A05", "A06"),

    # Columns
    ("A06", "A07"),
    ("A07", "A08"),

    # Slab
    ("A08", "A09"),
    ("A09", "A10"),

    # Masonry can start after columns
    ("A08", "A11"),

    # MEP rough-in after masonry
    ("A11", "A12"),

    # Plastering after masonry
    ("A11", "A13"),

    # Flooring & ceiling after plastering + MEP
    ("A13", "A14"),
    ("A12", "A14"),

    # Final finishes
    ("A14", "A15"),
]


for predecessor_code, successor_code in dependencies:

    dependency = Dependency(
        predecessor_id=activity_objects[
            predecessor_code
        ].id,

        successor_id=activity_objects[
            successor_code
        ].id,

        lag_days=0
    )

    db.add(dependency)


db.commit()

print("Dependencies created successfully.")


# =========================================================
# FINISH
# =========================================================

db.close()

print("\nREALISTIC BUILDING PROJECT SETUP COMPLETE")
print(f"Project ID: {PROJECT_ID}")