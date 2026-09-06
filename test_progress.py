from datetime import date

from database import SessionLocal
from models import Activity
from progress import analyze_activity_progress


db = SessionLocal()


activity = db.query(Activity).filter(
    Activity.name == "Pile Cap RCC"
).first()


if activity is None:
    print("Activity not found.")
else:

    result = analyze_activity_progress(
        activity,
        date(2026, 9, 12)
    )

    print("\nPROJECT PROGRESS ANALYSIS")
    print("-------------------------")

    for key, value in result.items():
        print(f"{key}: {value}")


db.close()