from database import SessionLocal
from models import Activity, Dependency, DelayEvent


def analyze_delay(activity_id):

    db = SessionLocal()

    try:

        # Find the delayed activity
        activity = db.query(Activity).filter(
            Activity.id == activity_id
        ).first()

        if not activity:
            return {
                "error": "Activity not found"
            }

        # Find delay events for this activity
        delays = db.query(DelayEvent).filter(
            DelayEvent.activity_id == activity_id
        ).all()

        total_delay = sum(
            delay.impact_days or 0
            for delay in delays
        )

        # -----------------------------------------
        # Find downstream affected activities
        # -----------------------------------------

        affected_activities = []

        visited = set()

        queue = [activity_id]

        while queue:

            current_id = queue.pop(0)

            if current_id in visited:
                continue

            visited.add(current_id)

            dependencies = db.query(Dependency).filter(
                Dependency.predecessor_id == current_id
            ).all()

            for dependency in dependencies:

                successor = db.query(Activity).filter(
                    Activity.id == dependency.successor_id
                ).first()

                if not successor:
                    continue

                affected_activities.append({
                    "Activity": successor.name,
                    "Critical": (
                        "YES"
                        if successor.is_critical
                        else "NO"
                    ),
                    "Float": successor.total_float
                })

                queue.append(successor.id)

        # -----------------------------------------
        # Estimate project impact
        # -----------------------------------------

        if activity.is_critical:
            project_impact = total_delay
        else:
            project_impact = 0

        return {
            "Delayed Activity": activity.name,
            "Total Delay": total_delay,
            "Critical Activity": (
                "YES"
                if activity.is_critical
                else "NO"
            ),
            "Potential Project Impact": project_impact,
            "Affected Activities": affected_activities
        }

    finally:

        db.close()