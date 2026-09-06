from database import SessionLocal
from models import Project, Activity


def find_activity(project_id: int, activity_name: str):

    db = SessionLocal()

    try:

        project = db.query(Project).filter(
            Project.id == project_id
        ).first()

        if not project:
            return {
                "error": "Project not found"
            }

        activities = db.query(Activity).filter(
            Activity.project_id == project_id
        ).all()

        search_name = activity_name.lower().strip()

        matches = []

        for activity in activities:

            if search_name in activity.name.lower():

                matches.append({
                    "Activity ID": activity.id,
                    "Activity": activity.name,
                    "Planned Start": str(activity.planned_start),
                    "Planned Finish": str(activity.planned_finish),
                    "Critical": bool(activity.is_critical)
                })

        if not matches:

            return {
                "Project": project.name,
                "Search": activity_name,
                "Match Count": 0,
                "Matches": []
            }

        return {
            "Project": project.name,
            "Search": activity_name,
            "Match Count": len(matches),
            "Matches": matches
        }

    finally:
        db.close()