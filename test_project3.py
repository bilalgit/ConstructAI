from database import SessionLocal
from models import Project, Activity, Dependency
from datetime import date


db = SessionLocal()


# =========================================================
# CREATE PROJECT 3
# =========================================================

project = Project(
    name="ConstructAI Building Control Demo"
)

db.add(project)
db.commit()
db.refresh(project)

PROJECT_ID = project.id

print(f"Project 3 created with ID: {PROJECT_ID}")


# =========================================================
# ACTIVITIES
# =========================================================

activities_data = [

    ("A01", "Site Mobilization", "Preliminaries", 3),
    ("A02", "Excavation", "Substructure", 5),
    ("A03", "PCC", "Substructure", 3),
    ("A04", "Footing Reinforcement", "Substructure", 5),
    ("A05", "Footing Concrete", "Substructure", 2),
    ("A06", "Pedestal Reinforcement", "Substructure", 3),
    ("A07", "Pedestal Concrete", "Substructure", 2),

    ("A08", "Column Reinforcement", "Superstructure", 5),
    ("A09", "Column Concrete", "Superstructure", 2),
    ("A10", "Slab Reinforcement", "Superstructure", 6),
    ("A11", "Slab Concrete", "Superstructure", 2),

    ("A12", "Masonry", "Architectural", 8),
    ("A13", "Electrical Rough-in", "MEP", 5),
    ("A14", "Plumbing Rough-in", "MEP", 5),

    ("A15", "Plastering", "Architectural", 7),
    ("A16", "Flooring", "Finishes", 6),
    ("A17", "False Ceiling", "Finishes", 5),
    ("A18", "Painting", "Finishes", 6),
    ("A19", "Final MEP Installation", "MEP", 4),
    ("A20", "Testing & Commissioning", "MEP", 3),
    ("A21", "Final Inspection & Handover", "Closeout", 2),
]


activity_objects = {}


for index, (code, name, category, duration) in enumerate(
    activities_data,
    start=1
):

    activity = Activity(
        project_id=PROJECT_ID,
        activity_code=code,
        name=name,
        wbs=f"1.{index}",
        category=category,
        unit="days",
        quantity=1,
        planned_start=date(2026, 9, 1),
        planned_finish=date(2026, 9, 1),
        planned_duration=duration,
        progress=0
    )

    db.add(activity)
    db.flush()

    activity_objects[code] = activity


db.commit()

print("21 activities created successfully.")


# =========================================================
# DEPENDENCIES
# =========================================================

dependencies = [

    # Preliminary → Excavation
    ("A01", "A02"),

    # Substructure
    ("A02", "A03"),
    ("A03", "A04"),
    ("A04", "A05"),
    ("A05", "A06"),
    ("A06", "A07"),

    # Superstructure
    ("A07", "A08"),
    ("A08", "A09"),
    ("A09", "A10"),
    ("A10", "A11"),

    # Masonry after slab
    ("A11", "A12"),

    # MEP rough-in after masonry
    ("A12", "A13"),
    ("A12", "A14"),

    # Plastering after masonry + rough-in
    ("A12", "A15"),
    ("A13", "A15"),
    ("A14", "A15"),

    # Finishes
    ("A15", "A16"),
    ("A15", "A17"),

    # Painting after plastering
    ("A15", "A18"),

    # Final MEP after rough-in
    ("A13", "A19"),
    ("A14", "A19"),

    # Testing after final MEP
    ("A19", "A20"),

    # Handover after all major finishes
    ("A16", "A21"),
    ("A17", "A21"),
    ("A18", "A21"),
    ("A20", "A21"),
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
db.close()


print("Dependencies created successfully.")
print()
print("PROJECT 3 SETUP COMPLETE")
print(f"Project ID: {PROJECT_ID}")