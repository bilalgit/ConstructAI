from database import SessionLocal
from models import Project, Activity, Dependency


def get_activity_dependencies(project_id: int, activity_id: int):

    db = SessionLocal()

    try:
        # -----------------------------------------
        # Check project
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
        # Check activity
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
        # Find predecessor dependencies
        # -----------------------------------------

        predecessor_dependencies = (
            db.query(Dependency)
            .filter(
                Dependency.successor_id == activity_id
            )
            .all()
        )

        predecessors = []

        for dependency in predecessor_dependencies:

            predecessor = (
                db.query(Activity)
                .filter(
                    Activity.id == dependency.predecessor_id,
                    Activity.project_id == project_id
                )
                .first()
            )

            if predecessor:

                predecessors.append({
                    "Activity ID": predecessor.id,
                    "Activity": predecessor.name,
                    "Dependency Type": dependency.dependency_type,
                    "Lag Days": dependency.lag_days
                })

        # -----------------------------------------
        # Find successor dependencies
        # -----------------------------------------

        successor_dependencies = (
            db.query(Dependency)
            .filter(
                Dependency.predecessor_id == activity_id
            )
            .all()
        )

        successors = []

        for dependency in successor_dependencies:

            successor = (
                db.query(Activity)
                .filter(
                    Activity.id == dependency.successor_id,
                    Activity.project_id == project_id
                )
                .first()
            )

            if successor:

                successors.append({
                    "Activity ID": successor.id,
                    "Activity": successor.name,
                    "Dependency Type": dependency.dependency_type,
                    "Lag Days": dependency.lag_days
                })

        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return {
            "Project": project.name,
            "Activity ID": activity.id,
            "Activity": activity.name,

            "Predecessor Count": len(predecessors),
            "Predecessors": predecessors,

            "Successor Count": len(successors),
            "Successors": successors
        }

    finally:
        db.close()