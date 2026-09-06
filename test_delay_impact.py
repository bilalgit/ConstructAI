from delay_impact import calculate_delay_impact


PROJECT_ID = 3

# Project 3:
# A13 = Electrical Rough-in
#
# Database ID for A13 is expected to be 19
ACTIVITY_ID = 33

DELAY_DAYS = 3


result = calculate_delay_impact(
    PROJECT_ID,
    ACTIVITY_ID,
    DELAY_DAYS
)


print("\n")
print("CONSTRUCTAI DELAY IMPACT ANALYSIS")
print("=================================")


if "error" in result:

    print(result["error"])

else:

    print(
        f"Delayed Activity: "
        f"{result['Delayed Activity']}"
    )

    print(
        f"Delay Applied: "
        f"{result['Delay Applied']} days"
    )

    print(
        f"Original Project Finish: "
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
        "\nAffected Activities:"
    )

    for activity in result[
        "Affected Activities"
    ]:

        print(
            f" - {activity}"
        )