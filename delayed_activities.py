from datetime import date

from database import SessionLocal
from models import Project, Activity


def get_delayed_activities(project_id: int):

    db = SessionLocal()

    try:
        # -----------------------------------------
        # Get project
        # -----------------------------------------

        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if not project:
            return {
                "error": "Project not found"
            }

        # -----------------------------------------
        # Get activities
        # -----------------------------------------

        activities = (
            db.query(Activity)
            .filter(Activity.project_id == project_id)
            .order_by(Activity.id)
            .all()
        )

        delayed = []

        today = date.today()

        for activity in activities:

            delay_days = 0
            delay_reason = None

            # -----------------------------------------
            # Case 1: Activity has actual finish
            # -----------------------------------------

            if (
                activity.actual_finish
                and activity.planned_finish
                and activity.actual_finish > activity.planned_finish
            ):

                delay_days = (
                    activity.actual_finish
                    - activity.planned_finish
                ).days

                delay_reason = "Completed after planned finish"

            # -----------------------------------------
            # Case 2: Activity has started but not finished
            # -----------------------------------------

            elif (
                activity.actual_start
                and not activity.actual_finish
                and activity.planned_finish
                and today > activity.planned_finish
            ):

                delay_days = (
                    today
                    - activity.planned_finish
                ).days

                delay_reason = "Activity not completed by planned finish"

            # -----------------------------------------
            # Case 3: Activity has not started
            # but planned finish has passed
            # -----------------------------------------

            elif (
                not activity.actual_start
                and not activity.actual_finish
                and activity.planned_finish
                and today > activity.planned_finish
            ):

                delay_days = (
                    today
                    - activity.planned_finish
                ).days

                delay_reason = "Activity has not started"

            # -----------------------------------------
            # Add delayed activity
            # -----------------------------------------

            if delay_days > 0:

                delayed.append({
                    "Activity ID": activity.id,
                    "Activity": activity.name,
                    "Planned Start": (
                        str(activity.planned_start)
                        if activity.planned_start
                        else None
                    ),
                    "Planned Finish": (
                        str(activity.planned_finish)
                        if activity.planned_finish
                        else None
                    ),
                    "Actual Start": (
                        str(activity.actual_start)
                        if activity.actual_start
                        else None
                    ),
                    "Actual Finish": (
                        str(activity.actual_finish)
                        if activity.actual_finish
                        else None
                    ),
                    "Delay Days": delay_days,
                    "Delay Reason": delay_reason,
                    "Total Float": (
                        activity.total_float
                        if activity.total_float is not None
                        else 0
                    ),
                    "Critical": bool(activity.is_critical)
                })

        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return {
            "Project": project.name,
            "Delayed Activity Count": len(delayed),
            "Delayed Activities": delayed
        }

    finally:
        db.close()