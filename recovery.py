from database import SessionLocal
from models import Activity


def calculate_recovery(activity_id, recovery_days):
    """
    Calculate the effect of recovering a specified number of days
    from an activity.
    """

    db = SessionLocal()

    try:
        activity = db.query(Activity).filter(
            Activity.id == activity_id
        ).first()

        if not activity:
            return {
                "error": "Activity not found"
            }

        if recovery_days <= 0:
            return {
                "error": "Recovery days must be greater than zero"
            }

        # Current planned duration
        original_duration = activity.planned_duration

        # Do not allow duration to become zero or negative
        maximum_recovery = max(
            original_duration - 1,
            0
        )

        actual_recovery = min(
            recovery_days,
            maximum_recovery
        )

        revised_duration = (
            original_duration - actual_recovery
        )

        return {
            "Activity": activity.name,
            "Original Duration": original_duration,
            "Requested Recovery": recovery_days,
            "Possible Recovery": actual_recovery,
            "Revised Duration": revised_duration,
            "Critical": (
                "YES"
                if activity.is_critical
                else "NO"
            ),
            "Total Float": activity.total_float
        }

    finally:
        db.close()