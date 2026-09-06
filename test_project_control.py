from project_control import analyze_project_delay


PROJECT_ID = 3

# Use the ID of Electrical Rough-in
ACTIVITY_ID = 33

DELAY_DAYS = 3

DELAY_REASON = "Material shortage"


result = analyze_project_delay(
    project_id=PROJECT_ID,
    activity_id=ACTIVITY_ID,
    delay_days=DELAY_DAYS,
    delay_reason=DELAY_REASON
)


print("\n")
print("CONSTRUCTAI PROJECT CONTROL REPORT")
print("==================================")


if "error" in result:

    print(result["error"])

else:

    print(f"\nActivity: {result['Activity']}")

    print(
        f"Delay Reason: "
        f"{result['Delay Reason']}"
    )

    print(
        f"Delay: "
        f"{result['Delay Days']} days"
    )

    print(
        f"\nOriginal Project Finish: "
        f"{result['Original Project Finish']}"
    )

    print(
        f"New Project Finish: "
        f"{result['New Project Finish']}"
    )

    print(
        f"Project Impact: "
        f"{result['Project Impact']} days"
    )

    print(
        f"Priority: "
        f"{result['Priority']}"
    )

    print("\nAffected Activities:")

    for activity in result[
        "Affected Activities"
    ]:

        print(f" - {activity}")

    print(
        "\nRecommended Action:"
    )

    print(
        result["Recommended Action"]
    )