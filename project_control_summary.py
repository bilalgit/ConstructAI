from database import SessionLocal
from models import Project, Activity


def get_project_control_summary(project_id: int):

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

        # -----------------------------------------
        # Basic project statistics
        # -----------------------------------------

        total_activities = len(activities)

        critical_activities = [
            a for a in activities
            if bool(a.is_critical)
        ]

        non_critical_activities = [
            a for a in activities
            if not bool(a.is_critical)
        ]

        zero_float_activities = [
            a for a in activities
            if a.total_float is None
            or a.total_float <= 0
        ]

        # -----------------------------------------
        # Project finish
        # -----------------------------------------

        planned_finishes = [
            a.planned_finish
            for a in activities
            if a.planned_finish
        ]

        project_finish = (
            max(planned_finishes)
            if planned_finishes
            else None
        )

        # -----------------------------------------
        # Delayed activities
        # -----------------------------------------

        delayed_activities = []

        for activity in activities:

            if (
                activity.actual_finish
                and activity.planned_finish
                and activity.actual_finish > activity.planned_finish
            ):

                delay = (
                    activity.actual_finish
                    - activity.planned_finish
                ).days

                delayed_activities.append({
                    "Activity ID": activity.id,
                    "Activity": activity.name,
                    "Delay Days": delay,
                    "Critical": bool(activity.is_critical)
                })

        # -----------------------------------------
        # Critical delayed activities
        # -----------------------------------------

        critical_delays = [
            a for a in delayed_activities
            if a["Critical"]
        ]

        # -----------------------------------------
        # Risk assessment
        # -----------------------------------------

        risk_score = 0

        critical_percentage = (
            len(critical_activities)
            / total_activities
        ) * 100

        zero_float_percentage = (
            len(zero_float_activities)
            / total_activities
        ) * 100

        if critical_percentage >= 70:
            risk_score += 3
        elif critical_percentage >= 50:
            risk_score += 2
        else:
            risk_score += 1

        if zero_float_percentage >= 70:
            risk_score += 3
        elif zero_float_percentage >= 50:
            risk_score += 2
        else:
            risk_score += 1

        if delayed_activities:
            risk_score += 2

        if critical_delays:
            risk_score += 3

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
                    d for d in delayed_activities
                    if d["Activity ID"] == activity.id
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
                    "Reasons": reasons
                })

        risk_activities.sort(
            key=lambda x: x["Risk Score"],
            reverse=True
        )

        # -----------------------------------------
        # Overall project control status
        # -----------------------------------------

        if critical_delays:

            control_status = "CRITICAL"

            overall_action = (
                "Immediate corrective action required. "
                "Critical-path activities are delayed."
            )

        elif delayed_activities:

            control_status = "AT RISK"

            overall_action = (
                "Review delayed activities and implement "
                "recovery measures where required."
            )

        elif risk_level == "HIGH":

            control_status = "AT RISK"

            overall_action = (
                "Maintain close monitoring of critical "
                "and zero-float activities."
            )

        else:

            control_status = "ON TRACK"

            overall_action = (
                "Project is currently under control. "
                "Continue routine monitoring."
            )

        # -----------------------------------------
        # Recommendations
        # -----------------------------------------

        recommendations = []

        if critical_delays:

            recommendations.append(
                "Prioritize delayed critical-path activities."
            )

        if zero_float_activities:

            recommendations.append(
                "Closely monitor zero-float activities."
            )

        if delayed_activities:

            recommendations.append(
                "Review causes of delay and implement "
                "appropriate recovery measures."
            )

        if not recommendations:

            recommendations.append(
                "Continue regular project monitoring "
                "and progress updates."
            )

        # -----------------------------------------
        # Return summary
        # -----------------------------------------

        return {
            "Project": project.name,
            "Project Control Status": control_status,
            "Project Finish": (
                str(project_finish)
                if project_finish
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

            "Highest Risk Activities":
                risk_activities[:10],

            "Delayed Activities":
                delayed_activities,

            "Recommendations":
                recommendations,

            "Overall Action":
                overall_action
        }

    finally:
        db.close()