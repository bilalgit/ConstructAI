from mcp.server import MCPServer
from project_status import get_project_status
from project_control import analyze_project_delay
from critical_activities import get_critical_activities
from activity_details import get_activity_details
from delayed_activities import get_delayed_activities
from activity_dependencies import get_activity_dependencies
from schedule_recovery import get_schedule_recovery
from resource_bottleneck import get_resource_bottleneck
from project_risk_analysis import get_project_risk_analysis
from project_control_summary import get_project_control_summary
from find_activity import find_activity

mcp = MCPServer("ConstructAI")


@mcp.tool()
def analyze_delay(
    project_id: int,
    activity_id: int,
    delay_days: int,
    delay_reason: str
) -> dict:
    """
    Analyze the impact of a construction activity delay.
    """

    return analyze_project_delay(
        project_id=project_id,
        activity_id=activity_id,
        delay_days=delay_days,
        delay_reason=delay_reason
    )

@mcp.tool()
def project_status(project_id: int) -> dict:
    """
    Get the current schedule status of a construction project.
    """

    return get_project_status(project_id)

@mcp.tool()
def critical_activities(project_id: int) -> dict:
    """
    Get all critical activities in a construction project.
    """

    return get_critical_activities(project_id)


@mcp.tool()
def activity_details(
    project_id: int,
    activity_id: int
) -> dict:
    return get_activity_details(
        project_id,
        activity_id
    )

@mcp.tool()
def delayed_activities(project_id: int) -> dict:
    """
    Find activities that are currently delayed.
    """
    return get_delayed_activities(project_id)


@mcp.tool()
def activity_dependencies(
    project_id: int,
    activity_id: int
) -> dict:
    """
    Get predecessor and successor dependencies
    for a construction activity.
    """
    return get_activity_dependencies(
        project_id,
        activity_id
    )

@mcp.tool()
def schedule_recovery(
    project_id: int,
    activity_id: int,
    delay_days: int
) -> dict:
    """
    Generate schedule recovery options for a delayed activity.
    """
    return get_schedule_recovery(
        project_id,
        activity_id,
        delay_days
    )

@mcp.tool()
def resource_bottleneck(project_id: int) -> dict:
    """
    Identify potential resource bottlenecks
    using project activity and schedule data.
    """
    return get_resource_bottleneck(project_id)

@mcp.tool()
def project_risk_analysis(project_id: int) -> dict:
    """
    Analyze overall project schedule risk.
    """
    return get_project_risk_analysis(project_id)

    
@mcp.tool()
def project_control_summary(project_id: int) -> dict:
    """
    Generate an overall construction project control summary.
    """
    return get_project_control_summary(project_id)

@mcp.tool()
def find_activity_tool(project_id: int, activity_name: str):
    """Find a construction activity by name in a project."""
    return find_activity(project_id, activity_name)

if __name__ == "__main__":
    mcp.run()

