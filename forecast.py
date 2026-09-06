from datetime import timedelta

from database import SessionLocal
from models import Activity, Dependency


def calculate_project_forecast(project_id):
    db = SessionLocal()

    try:
        activities = db.query(Activity).filter(
            Activity.project_id == project_id
        ).all()

        if not activities:
            return {
                "error": "No activities found"
            }

        activity_map = {
            activity.id: activity
            for activity in activities
        }

        dependencies = db.query(Dependency).all()

        # -----------------------------------------
        # Find baseline project completion
        # -----------------------------------------

        baseline_finish = max(
            activity.planned_finish
            for activity in activities
            if activity.planned_finish
        )

        # -----------------------------------------
        # Determine latest known/forecast finish
        # -----------------------------------------

        forecast_dates = []

        for activity in activities:

            # If actual finish exists, use it
            if activity.actual_finish:

                forecast_dates.append(
                    activity.actual_finish
                )

            # Otherwise use CPM early finish
            elif activity.early_finish:

                forecast_dates.append(
                    activity.early_finish
                )

            # Otherwise use planned finish
            elif activity.planned_finish:

                forecast_dates.append(
                    activity.planned_finish
                )

        if not forecast_dates:

            return {
                "error": "Unable to determine project forecast"
            }

        forecast_finish = max(forecast_dates)

        # -----------------------------------------
        # Calculate project delay
        # -----------------------------------------

        project_delay = (
            forecast_finish - baseline_finish
        ).days

        if project_delay > 0:

            status = "Delayed"

        elif project_delay < 0:

            status = "Ahead"

        else:

            status = "On Schedule"

        return {
            "Baseline Project Finish": baseline_finish,
            "Forecast Project Finish": forecast_finish,
            "Project Variance": project_delay,
            "Status": status
        }

    finally:
        db.close()
        