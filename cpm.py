from datetime import timedelta

from database import SessionLocal
from models import Activity, Dependency


def calculate_cpm(project_id):

    db = SessionLocal()

    try:

        activities = db.query(Activity).filter(
            Activity.project_id == project_id
        ).all()

        if not activities:
            return []

        activity_map = {
            activity.id: activity
            for activity in activities
        }

        dependencies = db.query(Dependency).all()

        # ==========================================
        # FORWARD PASS
        # ==========================================

        remaining = set(activity_map.keys())

        while remaining:

            progress_made = False

            for activity_id in list(remaining):

                activity = activity_map[activity_id]

                predecessors = [
                    d for d in dependencies
                    if d.successor_id == activity_id
                    and d.predecessor_id in activity_map
                ]

                # No predecessors
                if not predecessors:

                    activity.early_start = activity.planned_start

                    activity.early_finish = (
                        activity.early_start
                        + timedelta(
                            days=activity.planned_duration
                        )
                    )

                    remaining.remove(activity_id)

                    progress_made = True

                    continue

                # Wait until predecessors are calculated
                if any(
                    activity_map[d.predecessor_id].early_finish is None
                    for d in predecessors
                ):
                    continue

                earliest_start = activity.planned_start

                for dependency in predecessors:

                    predecessor = activity_map[
                        dependency.predecessor_id
                    ]

                    candidate_start = (
                        predecessor.early_finish
                        + timedelta(
                            days=dependency.lag_days
                        )
                    )

                    if candidate_start > earliest_start:
                        earliest_start = candidate_start

                activity.early_start = earliest_start

                activity.early_finish = (
                    activity.early_start
                    + timedelta(
                        days=activity.planned_duration
                    )
                )

                remaining.remove(activity_id)

                progress_made = True

            if not progress_made:

                raise ValueError(
                    "Circular dependency detected in project schedule."
                )

        # ==========================================
        # PROJECT FINISH
        # ==========================================

        project_finish = max(
            activity.early_finish
            for activity in activities
        )

        # ==========================================
        # BACKWARD PASS
        # ==========================================

        remaining = set(activity_map.keys())

        while remaining:

            progress_made = False

            for activity_id in list(remaining):

                activity = activity_map[activity_id]

                successors = [
                    d for d in dependencies
                    if d.predecessor_id == activity_id
                    and d.successor_id in activity_map
                ]

                # No successors
                if not successors:

                    activity.late_finish = project_finish

                    activity.late_start = (
                        activity.late_finish
                        - timedelta(
                            days=activity.planned_duration
                        )
                    )

                    remaining.remove(activity_id)

                    progress_made = True

                    continue

                # Wait until successors are calculated
                if any(
                    activity_map[d.successor_id].late_start is None
                    for d in successors
                ):
                    continue

                latest_finish = project_finish

                for dependency in successors:

                    successor = activity_map[
                        dependency.successor_id
                    ]

                    candidate_finish = (
                        successor.late_start
                        - timedelta(
                            days=dependency.lag_days
                        )
                    )

                    if candidate_finish < latest_finish:
                        latest_finish = candidate_finish

                activity.late_finish = latest_finish

                activity.late_start = (
                    activity.late_finish
                    - timedelta(
                        days=activity.planned_duration
                    )
                )

                remaining.remove(activity_id)

                progress_made = True

            if not progress_made:

                raise ValueError(
                    "Circular dependency detected in project schedule."
                )

        # ==========================================
        # FLOAT + CRITICAL PATH
        # ==========================================

        results = []

        for activity in activities:

            total_float = (
                activity.late_start -
                activity.early_start
            ).days

            is_critical = 1 if total_float <= 0 else 0

            # Save to database
            activity.total_float = total_float
            activity.is_critical = is_critical

            # Copy results BEFORE closing session
            results.append({
                "Activity": activity.name,
                "Early Start": activity.early_start,
                "Early Finish": activity.early_finish,
                "Late Start": activity.late_start,
                "Late Finish": activity.late_finish,
                "Total Float": total_float,
                "Critical": "YES" if is_critical else "NO"
            })

        db.commit()

        return results

    finally:

        db.close()