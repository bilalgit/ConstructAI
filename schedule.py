from datetime import timedelta

from database import SessionLocal
from models import Activity, Dependency


def get_predecessors(db, activity_id):
    """
    Return all predecessor activities for an activity.
    """

    dependencies = db.query(Dependency).filter(
        Dependency.successor_id == activity_id
    ).all()

    predecessors = []

    for dependency in dependencies:

        activity = db.query(Activity).filter(
            Activity.id == dependency.predecessor_id
        ).first()

        if activity:
            predecessors.append(
                {
                    "activity": activity,
                    "dependency": dependency
                }
            )

    return predecessors


def calculate_earliest_start(
    db,
    activity
):
    """
    Calculate the earliest possible start
    based on predecessor relationships.
    """

    predecessors = get_predecessors(
        db,
        activity.id
    )

    if not predecessors:
        return activity.planned_start

    earliest_start = activity.planned_start

    for item in predecessors:

        predecessor = item["activity"]
        dependency = item["dependency"]

        if predecessor.planned_finish is None:
            continue

        candidate_start = (
            predecessor.planned_finish
            + timedelta(days=dependency.lag_days)
        )

        if candidate_start > earliest_start:
            earliest_start = candidate_start

    return earliest_start


def calculate_schedule_shift(
    db,
    activity
):
    """
    Compare baseline start with dependency-driven start.
    """

    earliest_start = calculate_earliest_start(
        db,
        activity
    )

    shift = (
        earliest_start -
        activity.planned_start
    ).days

    return {
        "Activity": activity.name,
        "Baseline Start": activity.planned_start,
        "Dependency Driven Start": earliest_start,
        "Schedule Shift": shift
    }