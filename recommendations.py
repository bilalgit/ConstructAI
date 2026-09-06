def generate_recommendation(
    activity_name,
    delay_reason,
    delay_days,
    project_impact
):

    reason = delay_reason.lower()

    # -----------------------------------------
    # Material-related delay
    # -----------------------------------------

    if "material" in reason or "material shortage" in reason:

        action = (
            "Expedite material procurement, "
            "confirm supplier delivery, and "
            "check alternative approved suppliers."
        )

        priority = "HIGH"

    # -----------------------------------------
    # Labour-related delay
    # -----------------------------------------

    elif (
        "labour" in reason
        or "labor" in reason
        or "manpower" in reason
    ):

        action = (
            "Increase manpower, review productivity, "
            "and allocate additional workers to the "
            "affected work front."
        )

        priority = "HIGH"

    # -----------------------------------------
    # Equipment-related delay
    # -----------------------------------------

    elif (
        "equipment" in reason
        or "machinery" in reason
        or "machine" in reason
    ):

        action = (
            "Arrange replacement equipment, "
            "prioritize equipment allocation, and "
            "minimize equipment downtime."
        )

        priority = "HIGH"

    # -----------------------------------------
    # Drawing / approval delay
    # -----------------------------------------

    elif (
        "drawing" in reason
        or "approval" in reason
        or "design" in reason
    ):

        action = (
            "Escalate pending approvals, coordinate "
            "with the design team, and establish a "
            "clear approval deadline."
        )

        priority = "HIGH"

    # -----------------------------------------
    # Weather delay
    # -----------------------------------------

    elif (
        "rain" in reason
        or "weather" in reason
    ):

        action = (
            "Reschedule weather-sensitive activities, "
            "use available indoor work fronts, and "
            "increase productivity during suitable "
            "working periods."
        )

        priority = "MEDIUM"

    # -----------------------------------------
    # Default
    # -----------------------------------------

    else:

        action = (
            "Investigate the root cause, review "
            "available resources, and prepare a "
            "recovery plan for the affected activity."
        )

        priority = "MEDIUM"

    # -----------------------------------------
    # Project impact adjustment
    # -----------------------------------------

    if project_impact > 0:

        priority = "CRITICAL"

        action += (
            " Since the delay affects project "
            "completion, prioritize this activity "
            "in the recovery plan."
        )

    return {
        "Activity": activity_name,
        "Delay Reason": delay_reason,
        "Delay Days": delay_days,
        "Project Impact": project_impact,
        "Priority": priority,
        "Recommended Action": action
    }