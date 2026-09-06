from database import SessionLocal
from models import Project, Activity


def get_critical_activities(project_id: int):

    db = SessionLocal()

    try:
        # Get project
        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if not project:
            return {
                "error": "Project not found"
            }

        # Get critical activities
        activities = (
            db.query(Activity)
            .filter(
                Activity.project_id == project_id,
                Activity.is_critical == True
            )
            .order_by(Activity.id)
            .all()
        )

        if not activities:
            return {
                "Project": project.name,
                "Critical Activities": [],
                "Message": "No critical activities found"
            }

        results = []

        for activity in activities:

            results.append({
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
                "Total Float": (
                    activity.total_float
                    if activity.total_float is not None
                    else 0
                ),
                "Critical": True
            })

        return {
            "Project": project.name,
            "Critical Activity Count": len(results),
            "Critical Activities": results
        }

    finally:
        db.close()