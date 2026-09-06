from datetime import timedelta

from database import SessionLocal
from models import Activity, Dependency


def calculate_recovery_impact(activity_id, recovery_days):

    db = SessionLocal()

    try:

        activities = db.query(Activity).all()
        dependencies = db.query(Dependency).all()

        activity_map = {
            activity.id: activity
            for activity in activities
        }

        if activity_id not in activity_map:
            return {
                "error": "Activity not found"
            }

        activity = activity_map[activity_id]

        if recovery_days <= 0:
            return {
                "error": "Recovery days must be greater than zero"
            }

        original_duration = activity.planned_duration

        revised_duration = max(
            original_duration - recovery_days,
            1
        )

        # -----------------------------------------
        # Save original durations
        # -----------------------------------------

        original_durations = {
            a.id: a.planned_duration
            for a in activities
        }

        # Apply temporary recovery
        activity.planned_duration = revised_duration

        # -----------------------------------------
        # Forward pass
        # -----------------------------------------

        remaining = set(activity_map.keys())

        while remaining:

            progress_made = False

            for current_id in list(remaining):

                current = activity_map[current_id]

                predecessors = [
                    d for d in dependencies
                    if d.successor_id == current_id
                    and d.predecessor_id in activity_map
                ]

                if not predecessors:

                    current.early_start = current.planned_start

                    current.early_finish = (
                        current.early_start
                        + timedelta(
                            days=current.planned_duration
                        )
                    )

                    remaining.remove(current_id)
                    progress_made = True

                    continue

                if any(
                    activity_map[d.predecessor_id].early_finish
                    is None
                    for d in predecessors
                ):
                    continue

                earliest_start = current.planned_start

                for dependency in predecessors:

                    predecessor = activity_map[
                        dependency.predecessor_id
                    ]

                    candidate = (
                        predecessor.early_finish
                        + timedelta(
                            days=dependency.lag_days
                        )
                    )

                    if candidate > earliest_start:
                        earliest_start = candidate

                current.early_start = earliest_start

                current.early_finish = (
                    current.early_start
                    + timedelta(
                        days=current.planned_duration
                    )
                )

                remaining.remove(current_id)
                progress_made = True

            if not progress_made:

                raise ValueError(
                    "Circular dependency detected."
                )

        # -----------------------------------------
        # Calculate revised project finish
        # -----------------------------------------

        revised_finish = max(
            a.early_finish
            for a in activities
        )

        # -----------------------------------------
        # Current baseline finish
        # -----------------------------------------

        baseline_finish = max(
            a.planned_finish
            for a in activities
            if a.planned_finish
        )

        current_forecast = max(
            (
                a.actual_finish
                if a.actual_finish
                else a.planned_finish
            )
            for a in activities
            if a.actual_finish or a.planned_finish
        )

        current_delay = (
            current_forecast - baseline_finish
        ).days

        revised_delay = (
            revised_finish - baseline_finish
        ).days

        days_recovered = (
            current_delay - revised_delay
        )

        return {
            "Activity": activity.name,
            "Original Duration": original_duration,
            "Recovery Applied": recovery_days,
            "Revised Duration": revised_duration,
            "Baseline Finish": baseline_finish,
            "Current Forecast": current_forecast,
            "Revised Forecast": revised_finish,
            "Current Delay": current_delay,
            "Revised Delay": revised_delay,
            "Days Recovered": days_recovered
        }

    finally:

        # Restore original durations
        for current_id, duration in original_durations.items():

            if current_id in activity_map:
                activity_map[
                    current_id
                ].planned_duration = duration

        db.rollback()

        db.close()