from datetime import date

from database import SessionLocal
from models import Activity


def calculate_finish_variance(activity):
    """
    Compare planned finish with actual finish.

    Positive value  = delayed
    Negative value  = ahead
    Zero             = on schedule
    """

    if not activity.planned_finish:
        return None

    if not activity.actual_finish:
        return None

    variance = (
        activity.actual_finish
        - activity.planned_finish
    ).days

    return variance


def get_schedule_status(variance):
    """
    Convert schedule variance into a readable status.
    """

    if variance is None:
        return "No Actual Finish"

    if variance > 0:
        return "Delayed"

    if variance < 0:
        return "Ahead"

    return "On Schedule"


def analyze_activity(activity):
    """
    Generate schedule variance information
    for one activity.
    """

    variance = calculate_finish_variance(activity)

    status = get_schedule_status(variance)

    return {
        "Activity": activity.name,
        "Planned Finish": activity.planned_finish,
        "Actual Finish": activity.actual_finish,
        "Variance Days": variance,
        "Status": status
    }


def analyze_project(project_id):
    """
    Analyze schedule variance for all activities
    belonging to a project.
    """

    db = SessionLocal()

    try:

        activities = db.query(Activity).filter(
            Activity.project_id == project_id
        ).all()

        results = []

        for activity in activities:

            result = analyze_activity(activity)

            results.append(result)

        return results

    finally:

        db.close()