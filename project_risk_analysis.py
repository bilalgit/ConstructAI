from datetime import date

from database import SessionLocal
from models import Project, Activity


def get_project_risk_analysis(project_id: int):

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
            .all()
        )

        if not activities:
            return {
                "error": "No activities found in this project"
            }

        total_activities = len(activities)

        critical_activities = [
            activity
            for activity in activities
            if bool(activity.is_critical)
        ]

        non_critical_activities = [
            activity
            for activity in activities
            if not bool(activity.is_critical)
        ]

        zero_float_activities = [
            activity
            for activity in activities
            if (
                activity.total_float is None
                or activity.total_float <= 0
            )
        ]

        # -----------------------------------------
        # Find delayed activities
        # -----------------------------------------

        today = date.today()

        delayed_activities = []

        for activity in activities:

            delay_days = 0

            # Completed late
            if (
                activity.actual_finish
                and activity.planned_finish
                and activity.actual_finish > activity.planned_finish
            ):

                delay_days = (
                    activity.actual_finish
                    - activity.planned_finish
                ).days

            # Started but not completed
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

            # Not started and planned finish passed
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

            if delay_days > 0:

                delayed_activities.append({
                    "Activity ID": activity.id,
                    "Activity": activity.name,
                    "Delay Days": delay_days,
                    "Critical": bool(activity.is_critical),
                    "Total Float": (
                        activity.total_float
                        if activity.total_float is not None
                        else 0
                    )
                })

        # -----------------------------------------
        # Critical delayed activities
        # -----------------------------------------

        critical_delays = [
            activity
            for activity in delayed_activities
            if activity["Critical"]
        ]

        # -----------------------------------------
        # Calculate risk score
        # -----------------------------------------

        risk_score = 0

        # High critical-path exposure
        critical_percentage = (
            len(critical_activities)
            / total_activities
        ) * 100

        if critical_percentage >= 70:
            risk_score += 3
        elif critical_percentage >= 50:
            risk_score += 2
        else:
            risk_score += 1

        # Zero float exposure
        zero_float_percentage = (
            len(zero_float_activities)
            / total_activities
        ) * 100

        if zero_float_percentage >= 70:
            risk_score += 3
        elif zero_float_percentage >= 50:
            risk_score += 2
        else:
            risk_score += 1

        # Delays
        if len(delayed_activities) > 0:
            risk_score += 2

        if len(critical_delays) > 0:
            risk_score += 3

        # -----------------------------------------
        # Determine risk level
        # -----------------------------------------

        if risk_score >= 8:
            risk_level = "HIGH"

        elif risk_score >= 5:
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"

        # -----------------------------------------
        # Highest-risk activities
        # -----------------------------------------

        risk_activities = []

        for activity in activities:

            score = 0
            reasons = []

            if bool(activity.is_critical):
                score += 3
                reasons.append(
                    "Critical-path activity"
                )

            total_float = (
                activity.total_float
                if activity.total_float is not None
                else 0
            )

            if total_float <= 0:
                score += 2
                reasons.append(
                    "Zero available float"
                )

            delayed = next(
                (
                    item
                    for item in delayed_activities
                    if item["Activity ID"] == activity.id
                ),
                None
            )

            if delayed:

                score += 3

                reasons.append(
                    f"Delayed by "
                    f"{delayed['Delay Days']} days"
                )

            if score >= 5:

                risk_activities.append({
                    "Activity ID": activity.id,
                    "Activity": activity.name,
                    "Risk Score": score,
                    "Critical": bool(activity.is_critical),
                    "Total Float": total_float,
                    "Reasons": reasons
                })

        risk_activities.sort(
            key=lambda x: x["Risk Score"],
            reverse=True
        )

        # -----------------------------------------
        # Recommendations
        # -----------------------------------------

        recommendations = []

        if critical_delays:

            recommendations.append(
                "Immediately prioritize delayed "
                "critical-path activities."
            )

        if zero_float_activities:

            recommendations.append(
                "Closely monitor zero-float activities "
                "because they have little or no schedule flexibility."
            )

        if critical_percentage >= 70:

            recommendations.append(
                "Maintain close control of critical-path "
                "activities and prevent further slippage."
            )

        if delayed_activities:

            recommendations.append(
                "Review delayed activities and implement "
                "recovery measures where required."
            )

        if not recommendations:

            recommendations.append(
                "Continue routine schedule monitoring "
                "and update actual progress regularly."
            )

        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return {
            "Project": project.name,
            "Project Finish": (
                str(
                    max(
                        activity.planned_finish
                        for activity in activities
                        if activity.planned_finish
                    )
                )
                if any(
                    activity.planned_finish
                    for activity in activities
                )
                else None
            ),
            "Total Activities": total_activities,
            "Critical Activities": len(
                critical_activities
            ),
            "Non-Critical Activities": len(
                non_critical_activities
            ),
            "Zero Float Activities": len(
                zero_float_activities
            ),
            "Delayed Activities": len(
                delayed_activities
            ),
            "Critical Delayed Activities": len(
                critical_delays
            ),
            "Risk Score": risk_score,
            "Overall Risk": risk_level,
            "Highest Risk Activities": risk_activities[:10],
            "Recommendations": recommendations
        }

    finally:
        db.close()