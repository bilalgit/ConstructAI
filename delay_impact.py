from datetime import timedelta

from database import SessionLocal
from models import Activity, Dependency


def calculate_delay_impact(project_id, activity_id, delay_days):

    db = SessionLocal()

    activities = []
    original_values = {}

    try:
        activities = db.query(Activity).filter(
            Activity.project_id == project_id
        ).all()

        dependencies = db.query(Dependency).all()

        activity_map = {
            activity.id: activity
            for activity in activities
        }

        if activity_id not in activity_map:
            return {
                "error": "Activity not found in this project"
            }

        if delay_days <= 0:
            return {
                "error": "Delay days must be greater than zero"
            }

        delayed_activity = activity_map[activity_id]

        # -------------------------------------------------
        # Save original values
        # -------------------------------------------------

        for activity in activities:
            original_values[activity.id] = {
                "early_start": activity.early_start,
                "early_finish": activity.early_finish,
            }

        # -------------------------------------------------
        # Original project finish
        # -------------------------------------------------

        original_finish = max(
            activity.early_finish
            for activity in activities
            if activity.early_finish
        )

        # -------------------------------------------------
        # Apply delay
        # -------------------------------------------------

        delayed_activity.early_finish = (
            delayed_activity.early_finish
            + timedelta(days=delay_days)
        )

        # -------------------------------------------------
        # Propagate delay through network
        # -------------------------------------------------

        changed = True

        while changed:

            changed = False

            for dependency in dependencies:

                if (
                    dependency.predecessor_id not in activity_map
                    or dependency.successor_id not in activity_map
                ):
                    continue

                predecessor = activity_map[
                    dependency.predecessor_id
                ]

                successor = activity_map[
                    dependency.successor_id
                ]

                if predecessor.early_finish is None:
                    continue

                possible_start = (
                    predecessor.early_finish
                    + timedelta(
                        days=dependency.lag_days
                    )
                )

                if (
                    successor.early_start is None
                    or possible_start > successor.early_start
                ):

                    successor.early_start = possible_start

                    successor.early_finish = (
                        successor.early_start
                        + timedelta(
                            days=successor.planned_duration
                        )
                    )

                    changed = True

        # -------------------------------------------------
        # New project finish
        # -------------------------------------------------

        new_finish = max(
            activity.early_finish
            for activity in activities
            if activity.early_finish
        )

        project_impact = (
            new_finish - original_finish
        ).days

        # -------------------------------------------------
        # Identify affected activities
        # -------------------------------------------------

        affected_activities = []

        for activity in activities:

            original_finish_date = (
                original_values[activity.id]["early_finish"]
            )

            if (
                activity.early_finish
                and original_finish_date
                and activity.early_finish
                > original_finish_date
            ):

                affected_activities.append(
                    activity.name
                )

        return {
            "Delayed Activity": delayed_activity.name,
            "Delay Applied": delay_days,
            "Original Project Finish": original_finish,
            "New Project Finish": new_finish,
            "Project Impact": project_impact,
            "Affected Activities": affected_activities,
        }

    finally:

        # -------------------------------------------------
        # Restore original values
        # -------------------------------------------------

        for activity in activities:

            if activity.id in original_values:

                activity.early_start = (
                    original_values[activity.id]["early_start"]
                )

                activity.early_finish = (
                    original_values[activity.id]["early_finish"]
                )

        db.rollback()
        db.close()