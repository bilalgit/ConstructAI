from database import SessionLocal
from models import Activity

from schedule import calculate_schedule_shift


db = SessionLocal()


activity = db.query(Activity).filter(
    Activity.name == "Pedestal RCC"
).first()


if activity is None:

    print("Activity not found.")

else:

    result = calculate_schedule_shift(
        db,
        activity
    )

    print("\nSCHEDULE ANALYSIS")
    print("------------------")

    for key, value in result.items():
        print(f"{key}: {value}")


db.close()