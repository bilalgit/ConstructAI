from database import SessionLocal
from models import Project, Activity


def get_project_status(project_id: int):

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

        if not activities:
            return {
                "error": "No activities found for this project"
            }

        # -----------------------------------------
        # Activity statistics
        # -----------------------------------------

        total_activities = len(activities)

        critical_activities = [
            activity
            for activity in activities
            if activity.is_critical
        ]

        non_critical_activities = [
            activity
            for activity in activities
            if not activity.is_critical
        ]

        # -----------------------------------------
        # Find project finish
        # -----------------------------------------

        project_finish_dates = [
            activity.planned_finish
            for activity in activities
            if activity.planned_finish is not None
        ]

        project_finish = (
            max(project_finish_dates)
            if project_finish_dates
            else None
        )

        # -----------------------------------------
        # Critical path
        # -----------------------------------------

        critical_path = [
            activity.name
            for activity in activities
            if activity.is_critical
        ]

        # -----------------------------------------
        # Highest-risk activities
        # -----------------------------------------

        risk_activities = sorted(
            critical_activities,
            key=lambda activity: (
                activity.total_float
                if activity.total_float is not None
                else 999999
            )
        )

        highest_risk = [
            activity.name
            for activity in risk_activities[:5]
        ]

        # -----------------------------------------
        # Return project status
        # -----------------------------------------

        return {

            "Project": project.name,

            "Project Finish":
                str(project_finish)
                if project_finish
                else None,

            "Total Activities":
                total_activities,

            "Critical Activities":
                len(critical_activities),

            "Non-Critical Activities":
                len(non_critical_activities),

            "Critical Path":
                critical_path,

            "Highest Risk Activities":
                highest_risk
        }

    finally:

        db.close()