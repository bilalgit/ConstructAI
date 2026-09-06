from datetime import date

from database import SessionLocal
from models import Activity


PROJECT_ID = 3


schedule = {
    21: ("2026-09-01", "2026-09-04"),  # Site Mobilization
    22: ("2026-09-04", "2026-09-09"),  # Excavation
    23: ("2026-09-09", "2026-09-12"),  # PCC
    24: ("2026-09-12", "2026-09-17"),  # Footing Reinforcement
    25: ("2026-09-17", "2026-09-19"),  # Footing Concrete
    26: ("2026-09-19", "2026-09-22"),  # Pedestal Reinforcement
    27: ("2026-09-22", "2026-09-24"),  # Pedestal Concrete
    28: ("2026-09-24", "2026-09-29"),  # Column Reinforcement
    29: ("2026-09-29", "2026-10-01"),  # Column Concrete
    30: ("2026-10-01", "2026-10-07"),  # Slab Reinforcement
    31: ("2026-10-07", "2026-10-09"),  # Slab Concrete
    32: ("2026-10-09", "2026-10-17"),  # Masonry
    33: ("2026-10-17", "2026-10-22"),  # Electrical Rough-in
    34: ("2026-10-17", "2026-10-22"),  # Plumbing Rough-in
    35: ("2026-10-22", "2026-10-29"),  # Plastering
    36: ("2026-10-29", "2026-11-04"),  # Flooring
    37: ("2026-10-29", "2026-11-03"),  # False Ceiling
    38: ("2026-10-29", "2026-11-04"),  # Painting
    39: ("2026-10-22", "2026-10-26"),  # Final MEP Installation
    40: ("2026-10-26", "2026-10-29"),  # Testing & Commissioning
    41: ("2026-11-04", "2026-11-06"),  # Final Inspection & Handover
}


db = SessionLocal()

try:
    activities = (
        db.query(Activity)
        .filter(
            Activity.project_id == PROJECT_ID,
            Activity.id.in_(schedule.keys())
        )
        .all()
    )

    for activity in activities:
        start_date, finish_date = schedule[activity.id]

        activity.planned_start = date.fromisoformat(start_date)
        activity.planned_finish = date.fromisoformat(finish_date)

    db.commit()

    print("Project 3 schedule dates updated successfully.")

finally:
    db.close()