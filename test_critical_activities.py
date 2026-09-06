from critical_activities import get_critical_activities


PROJECT_ID = 3


result = get_critical_activities(PROJECT_ID)


print("\n")
print("CONSTRUCTAI CRITICAL ACTIVITIES")
print("===============================")

if "error" in result:

    print(result["error"])

else:

    print(
        f"\nProject: "
        f"{result['Project']}"
    )

    print(
        f"Critical Activity Count: "
        f"{result['Critical Activity Count']}"
    )

    print("\nCritical Activities:")

    for activity in result["Critical Activities"]:

        print(
            f"\nID: {activity['Activity ID']}"
        )

        print(
            f"Activity: {activity['Activity']}"
        )

        print(
            f"Planned Start: "
            f"{activity['Planned Start']}"
        )

        print(
            f"Planned Finish: "
            f"{activity['Planned Finish']}"
        )

        print(
            f"Total Float: "
            f"{activity['Total Float']} days"
        )

        print(
            f"Critical: "
            f"{activity['Critical']}"
        )