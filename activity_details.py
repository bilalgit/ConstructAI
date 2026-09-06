from database import SessionLocal
from models import Project, Activity


def get_activity_details(project_id: int, activity_id: int):

    db = SessionLocal()

    try:
        # -----------------------------------------
        # Get activity
        # -----------------------------------------

        activity = (
            db.query(Activity)
            .filter(
                Activity.id == activity_id,
                Activity.project_id == project_id
            )
            .first()
        )

        if not activity:
            return {
                "error": "Activity not found in this project"
            }

        # -----------------------------------------
        # Get project
        # -----------------------------------------

        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        # -----------------------------------------
        # Activity details
        # -----------------------------------------

        return {
            "Project": project.name if project else None,

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

            "Planned Duration": activity.planned_duration,

            "Actual Duration": activity.actual_duration,

            "Total Float": (
                activity.total_float
                if activity.total_float is not None
                else 0
            ),

            "Critical": bool(activity.is_critical)
        }

    finally:
        db.close()