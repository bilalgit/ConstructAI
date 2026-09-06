from datetime import date


def calculate_planned_progress(
    planned_start,
    planned_finish,
    as_of_date
):
    """
    Calculate expected progress based on elapsed planned duration.
    """

    if as_of_date < planned_start:
        return 0.0

    if as_of_date >= planned_finish:
        return 100.0

    total_days = (planned_finish - planned_start).days
    elapsed_days = (as_of_date - planned_start).days

    if total_days <= 0:
        return 100.0

    progress = (elapsed_days / total_days) * 100

    return round(progress, 2)


def calculate_progress_variance(
    planned_progress,
    actual_progress
):
    """
    Calculate progress variance.
    Positive = ahead
    Negative = behind
    """

    variance = actual_progress - planned_progress

    return round(variance, 2)


def analyze_activity_progress(
    activity,
    as_of_date
):
    """
    Compare planned and actual progress for an activity.
    """

    planned_progress = calculate_planned_progress(
        activity.planned_start,
        activity.planned_finish,
        as_of_date
    )

    actual_progress = activity.progress or 0.0

    variance = calculate_progress_variance(
        planned_progress,
        actual_progress
    )

    if variance > 0:
        status = "Ahead"
    elif variance < 0:
        status = "Behind"
    else:
        status = "On Schedule"

    return {
        "Activity": activity.name,
        "Planned Progress": planned_progress,
        "Actual Progress": actual_progress,
        "Variance": variance,
        "Status": status
    }