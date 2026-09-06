from database import SessionLocal
from models import Project, Activity


def get_resource_bottleneck(project_id: int):

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
                "error": "No activities found in this project"
            }

        bottlenecks = []

        for activity in activities:

            quantity = (
                activity.quantity
                if activity.quantity is not None
                else 0
            )

            progress = (
                activity.progress
                if activity.progress is not None
                else 0
            )

            total_float = (
                activity.total_float
                if activity.total_float is not None
                else 0
            )

            critical = bool(activity.is_critical)

            planned_duration = (
                activity.planned_duration
                if activity.planned_duration is not None
                else 0
            )

            # -----------------------------------------
            # Calculate bottleneck score
            # -----------------------------------------

            score = 0
            reasons = []

            # Critical activity
            if critical:
                score += 3
                reasons.append(
                    "Critical-path activity"
                )

            # No float
            if total_float <= 0:
                score += 2
                reasons.append(
                    "No available float"
                )

            # Large quantity
            if quantity > 0:
                score += 1
                reasons.append(
                    "Activity has measurable workload"
                )

            # Low progress on longer activity
            if (
                planned_duration >= 5
                and progress < 50
            ):
                score += 2
                reasons.append(
                    "Low progress on a relatively long activity"
                )

            # Very low progress
            if progress < 25:
                score += 1
                reasons.append(
                    "Very low progress"
                )

            # -----------------------------------------
            # Classify bottleneck
            # -----------------------------------------

            if score >= 6:
                risk_level = "HIGH"

            elif score >= 4:
                risk_level = "MEDIUM"

            else:
                risk_level = "LOW"

            # -----------------------------------------
            # Only report meaningful bottlenecks
            # -----------------------------------------

            if score >= 4:

                bottlenecks.append({
                    "Activity ID": activity.id,
                    "Activity": activity.name,
                    "Category": activity.category,
                    "Quantity": quantity,
                    "Unit": activity.unit,
                    "Progress": progress,
                    "Planned Duration": planned_duration,
                    "Total Float": total_float,
                    "Critical": critical,
                    "Bottleneck Score": score,
                    "Risk Level": risk_level,
                    "Reasons": reasons
                })

        # -----------------------------------------
        # Sort highest risk first
        # -----------------------------------------

        bottlenecks.sort(
            key=lambda x: x["Bottleneck Score"],
            reverse=True
        )

        # -----------------------------------------
        # Recommendation
        # -----------------------------------------

        if bottlenecks:

            high_count = sum(
                1
                for item in bottlenecks
                if item["Risk Level"] == "HIGH"
            )

            if high_count > 0:
                recommendation = (
                    "Prioritize HIGH-risk activities, "
                    "verify manpower and material availability, "
                    "and monitor critical-path activities closely."
                )
            else:
                recommendation = (
                    "Monitor the identified activities and "
                    "confirm that required resources are available."
                )

        else:

            recommendation = (
                "No significant resource bottlenecks "
                "were identified from the available activity data."
            )

        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return {
            "Project": project.name,
            "Bottleneck Count": len(bottlenecks),
            "Potential Bottlenecks": bottlenecks,
            "Recommendation": recommendation
        }

    finally:
        db.close()