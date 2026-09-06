from activity_details import get_activity_details


PROJECT_ID = 3
ACTIVITY_ID = 33


result = get_activity_details(
    PROJECT_ID,
    ACTIVITY_ID
)


print()
print("CONSTRUCTAI ACTIVITY DETAILS")
print("============================")


if "error" in result:

    print(result["error"])

else:

    print(f"Project: {result['Project']}")
    print(f"Activity ID: {result['Activity ID']}")
    print(f"Activity: {result['Activity']}")

    print(
        f"Planned Start: "
        f"{result['Planned Start']}"
    )

    print(
        f"Planned Finish: "
        f"{result['Planned Finish']}"
    )

    print(
        f"Actual Start: "
        f"{result['Actual Start']}"
    )

    print(
        f"Actual Finish: "
        f"{result['Actual Finish']}"
    )

    print(
        f"Planned Duration: "
        f"{result['Planned Duration']} days"
    )

    print(
        f"Actual Duration: "
        f"{result['Actual Duration']} days"
    )

    print(
        f"Total Float: "
        f"{result['Total Float']} days"
    )

    print(
        f"Critical: "
        f"{result['Critical']}"
    )