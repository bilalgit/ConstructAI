from database import SessionLocal
from models import Activity


def analyze_bottlenecks(project_id):

    db = SessionLocal()

    try:

        activities = db.query(Activity).filter(
            Activity.project_id == project_id
        ).all()

        if not activities:
            return {
                "error": "No activities found"
            }

        bottlenecks = []

        for activity in activities:

            float_days = activity.total_float

            if float_days is None:
                continue

            # Critical activities
            if float_days <= 0:

                risk = "HIGH"

            # Near-critical activities
            elif float_days <= 2:

                risk = "MEDIUM"

            else:

                risk = "LOW"

            bottlenecks.append({
                "Activity": activity.name,
                "Float": float_days,
                "Critical": (
                    "YES"
                    if activity.is_critical
                    else "NO"
                ),
                "Risk": risk
            })

        # Highest-risk activities first
        bottlenecks.sort(
            key=lambda x: x["Float"]
        )

        return bottlenecks

    finally:

        db.close()