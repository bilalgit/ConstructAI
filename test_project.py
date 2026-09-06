from datetime import date

from database import SessionLocal
from models import Project, Activity, Dependency, DelayEvent


db = SessionLocal()


# -----------------------------------
# 1. Create Project
# -----------------------------------

project = Project(
    name="Demo Commercial Building",
    location="Demo Location",
    contract_value=85000000,
    start_date=date(2026, 9, 1),
    planned_duration=365
)

db.add(project)
db.commit()
db.refresh(project)


print(f"Project created with ID: {project.id}")


# -----------------------------------
# 2. Create Activities
# -----------------------------------

excavation = Activity(
    project_id=project.id,
    activity_code="SUB-001",
    name="Excavation",
    wbs="1.1",
    category="Substructure",
    unit="m3",
    quantity=500,
    planned_start=date(2026, 9, 1),
    planned_finish=date(2026, 9, 5),
    planned_duration=5,
    progress=100
)


pcc = Activity(
    project_id=project.id,
    activity_code="SUB-002",
    name="PCC",
    wbs="1.2",
    category="Substructure",
    unit="m3",
    quantity=50,
    planned_start=date(2026, 9, 6),
    planned_finish=date(2026, 9, 8),
    planned_duration=3,
    progress=100
)


pile_cap = Activity(
    project_id=project.id,
    activity_code="SUB-003",
    name="Pile Cap RCC",
    wbs="1.3",
    category="Substructure",
    unit="m3",
    quantity=80,
    planned_start=date(2026, 9, 9),
    planned_finish=date(2026, 9, 15),
    planned_duration=7,
    progress=65
)


pedestal = Activity(
    project_id=project.id,
    activity_code="SUB-004",
    name="Pedestal RCC",
    wbs="1.4",
    category="Substructure",
    unit="m3",
    quantity=30,
    planned_start=date(2026, 9, 16),
    planned_finish=date(2026, 9, 19),
    planned_duration=4,
    progress=0
)


column = Activity(
    project_id=project.id,
    activity_code="STR-001",
    name="Column RCC",
    wbs="2.1",
    category="Superstructure",
    unit="m3",
    quantity=40,
    planned_start=date(2026, 9, 20),
    planned_finish=date(2026, 9, 25),
    planned_duration=6,
    progress=0
)


db.add_all([
    excavation,
    pcc,
    pile_cap,
    pedestal,
    column
])

db.commit()

print("Activities created successfully.")


# -----------------------------------
# 3. Create Dependencies
# -----------------------------------

dependencies = [

    Dependency(
        predecessor_id=excavation.id,
        successor_id=pcc.id,
        dependency_type="FS",
        lag_days=0
    ),

    Dependency(
        predecessor_id=pcc.id,
        successor_id=pile_cap.id,
        dependency_type="FS",
        lag_days=0
    ),

    Dependency(
        predecessor_id=pile_cap.id,
        successor_id=pedestal.id,
        dependency_type="FS",
        lag_days=0
    ),

    Dependency(
        predecessor_id=pedestal.id,
        successor_id=column.id,
        dependency_type="FS",
        lag_days=0
    )
]


db.add_all(dependencies)
db.commit()

print("Dependencies created successfully.")


# -----------------------------------
# 4. Create a Delay Event
# -----------------------------------

delay = DelayEvent(
    activity_id=pile_cap.id,
    delay_date=date(2026, 9, 12),
    category="Material",
    description="Concrete supply was unavailable for scheduled concreting.",
    duration_days=1,
    impact_days=1
)


db.add(delay)
db.commit()

print("Delay event created successfully.")


# -----------------------------------
# Finished
# -----------------------------------

db.close()

print("Demo project setup completed successfully.")