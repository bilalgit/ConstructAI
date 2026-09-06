from delay_impact import calculate_delay_impact
from recommendations import generate_recommendation


def analyze_project_delay(
    project_id,
    activity_id,
    delay_days,
    delay_reason
):

    # -----------------------------------------
    # STEP 1: Calculate delay impact
    # -----------------------------------------

    impact = calculate_delay_impact(
        project_id,
        activity_id,
        delay_days
    )

    if "error" in impact:
        return impact

    # -----------------------------------------
    # STEP 2: Generate recommendation
    # -----------------------------------------

    recommendation = generate_recommendation(
        activity_name=impact["Delayed Activity"],
        delay_reason=delay_reason,
        delay_days=delay_days,
        project_impact=impact["Project Impact"]
    )

    # -----------------------------------------
    # STEP 3: Combine results
    # -----------------------------------------

    report = {

        "Activity": impact["Delayed Activity"],

        "Delay Reason": delay_reason,

        "Delay Days": delay_days,

        "Original Project Finish":
            impact["Original Project Finish"],

        "New Project Finish":
            impact["New Project Finish"],

        "Project Impact":
            impact["Project Impact"],

        "Priority":
            recommendation["Priority"],

        "Affected Activities":
            impact["Affected Activities"],

        "Recommended Action":
            recommendation["Recommended Action"]
    }

    return report