from database import SessionLocal
from models import Project, Activity


def get_schedule_recovery(
    project_id: int,
    activity_id: int,
    delay_days: int
):

    db = SessionLocal()

    try:
        # -----------------------------------------
        # Validate delay
        # -----------------------------------------

        if delay_days <= 0:
            return {
                "error": "Delay days must be greater than 0"
            }

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
        # Get float
        # -----------------------------------------

        total_float = (
            activity.total_float
            if activity.total_float is not None
            else 0
        )

        critical = bool(activity.is_critical)

        # -----------------------------------------
        # Calculate unrecoverable impact
        # -----------------------------------------

        if critical:
            project_impact = delay_days
        else:
            project_impact = max(
                0,
                delay_days - total_float
            )

        # -----------------------------------------
        # Recovery options
        # -----------------------------------------

        options = []

        if delay_days >= 1:
            options.append({
                "Action": "Expedite material procurement",
                "Purpose": "Reduce waiting time for materials"
            })

        if delay_days >= 2:
            options.append({
                "Action": "Increase manpower",
                "Purpose": "Increase daily production"
            })

        if delay_days >= 2:
            options.append({
                "Action": "Increase working hours",
                "Purpose": "Recover lost working days"
            })

        if not critical and total_float >= delay_days:
            options.append({
                "Action": "Use available float",
                "Purpose": "Absorb the delay without affecting project finish"
            })

        if critical:
            options.append({
                "Action": "Prioritize critical-path activity",
                "Purpose": "Prevent further project completion delay"
            })

        options.append({
            "Action": "Coordinate successor activities",
            "Purpose": "Identify opportunities for controlled activity overlap"
        })

        # -----------------------------------------
        # Recommended strategy
        # -----------------------------------------

        if critical and delay_days >= 3:

            recommendation = (
                "Prioritize the critical activity, expedite materials, "
                "increase manpower where practical, and coordinate "
                "successor activities to recover lost time."
            )

        elif critical:

            recommendation = (
                "Prioritize the critical activity and use additional "
                "resources or working hours to recover the delay."
            )

        elif delay_days <= total_float:

            recommendation = (
                "Use the available float to absorb the delay. "
                "No immediate project-level recovery action is required."
            )

        else:

            recommendation = (
                "The delay exceeds available float. Increase resources "
                "or working hours and coordinate successor activities "
                "to minimize project impact."
            )

        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return {
            "Project": project.name,
            "Activity ID": activity.id,
            "Activity": activity.name,
            "Delay Days": delay_days,
            "Total Float": total_float,
            "Critical": critical,
            "Project Impact": project_impact,
            "Recovery Required": project_impact > 0,
            "Recovery Options": options,
            "Recommended Strategy": recommendation
        }

    finally:
        db.close()