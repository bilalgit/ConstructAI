from datetime import date

from database import SessionLocal
from models import Activity

from schedule_variance import analyze_project


PROJECT_ID = 1


db = SessionLocal()


# ---------------------------------------
# Add actual finish dates
# ---------------------------------------

pile_cap = db.query(Activity).filter(
    Activity.name == "Pile Cap RCC",
    Activity.project_id == PROJECT_ID
).first()


pedestal = db.query(Activity).filter(
    Activity.name == "Pedestal RCC",
    Activity.project_id == PROJECT_ID
).first()


column = db.query(Activity).filter(
    Activity.name == "Column RCC",
    Activity.project_id == PROJECT_ID
).first()


# Simulated actual dates

if pile_cap:
    pile_cap.actual_start = date(2026, 9, 10)
    pile_cap.actual_finish = date(2026, 9, 18)


if pedestal:
    pedestal.actual_start = date(2026, 9, 19)
    pedestal.actual_finish = date(2026, 9, 21)


if column:
    column.actual_start = date(2026, 9, 22)
    column.actual_finish = date(2026, 9, 27)


db.commit()
db.close()


# ---------------------------------------
# Analyze schedule
# ---------------------------------------

results = analyze_project(PROJECT_ID)


print("\n")
print("CONSTRUCTAI SCHEDULE VARIANCE")
print("==============================")


for result in results:

    print(f"\nActivity: {result['Activity']}")
    print(
        f"Planned Finish: "
        f"{result['Planned Finish']}"
    )

    print(
        f"Actual Finish:  "
        f"{result['Actual Finish']}"
    )

    print(
        f"Variance:        "
        f"{result['Variance Days']} days"
    )

    print(
        f"Status:          "
        f"{result['Status']}"
    )